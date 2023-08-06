import cli_ui
import sqlite3
import random
import ipaddress
import os
import subprocess
import qrcode
import io
import shutil
import darkdetect
from pathlib import Path


class Manager:
    def __init__(self):
        db_name = 'wgman1ton.db'
        Path(db_name).touch(mode=0o600, exist_ok=True)
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS hosts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, ip TEXT, private_key TEXT, public_key TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT, value TEXT)")
        self.con.commit()

        if self.cur.execute('SELECT * FROM settings WHERE key = "external_host_name"').fetchall():
            self.cur.execute('DELETE FROM settings WHERE key = "hostname"')
            self.cur.execute('UPDATE settings SET key = "hostname" WHERE key = "external_host_name"')

        if not self.cur.execute('SELECT * FROM settings').fetchall():
            print("initialize settings")
            self.cur.execute("INSERT INTO settings VALUES ('hostname','localhost')")
            self.cur.execute("INSERT INTO settings VALUES ('ip','10.10.0.1')")
            self.cur.execute("INSERT INTO settings VALUES ('ip_mask','24')")
            self.cur.execute("INSERT INTO settings VALUES ('listen_port','51820')")
            self.cur.execute("INSERT INTO settings VALUES ('persistent_keepalive','20')")

            private_key = subprocess.check_output(["wg", "genkey"]).decode("utf-8").strip()
            params = (private_key, )
            self.cur.execute("INSERT INTO settings VALUES ('host_private_key', ?)", params)

            p = subprocess.Popen(['wg', 'pubkey'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            public_key = p.communicate(input=private_key.encode())[0].decode().strip()
            params = (public_key, )
            self.cur.execute("INSERT INTO settings VALUES ('host_public_key', ?)", params)

            self.con.commit()

    def execute(self):
        cli_ui.setup()

        while True:
            main_menu_choices = ["edit general settings", "add node", "remove node", "display qr-code for node", "export all configs", "exit"]

            main_menu = cli_ui.ask_choice("Select an option", choices=main_menu_choices, sort=False)
            if main_menu == "edit general settings":
                while True:
                    choices = self.cur.execute('SELECT * FROM settings WHERE key !="host_private_key" AND key !="host_public_key"').fetchall()
                    choices.append('exit')
                    sub_menu = cli_ui.ask_choice("Select an option", choices=choices, sort=False)
                    if sub_menu == "exit":
                        break
                    if sub_menu:
                        parameter = tuple(sub_menu)[0]
                        old_value = tuple(sub_menu)[1]
                        new_value = cli_ui.ask_string("Please enter new value for", parameter, "[", old_value, "]")
                        if new_value:
                            params = (new_value, parameter)
                            query = """UPDATE settings SET value=? WHERE key=?"""
                            self.cur.execute(query, params)
                            self.con.commit()
            if main_menu == "add node":
                all_hosts = [r[0] for r in self.cur.execute('SELECT name FROM hosts').fetchall()]
                while True:
                    new_host = cli_ui.ask_string("Please enter new hostname (empty for abort)")
                    if new_host:
                        if new_host not in all_hosts:
                            private_key = subprocess.check_output(["wg", "genkey"]).decode("utf-8").strip()
                            p = subprocess.Popen(['wg', 'pubkey'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                            public_key = p.communicate(input=private_key.encode())[0].decode().strip()

                            params = (new_host, self.get_unused_ip(), private_key, public_key)
                            query = """INSERT INTO hosts(name, ip, private_key, public_key) VALUES (?,?,?,?)"""
                            self.cur.execute(query, params)
                            self.con.commit()
                            break
                        else:
                            print("Hostname is already taken")
                    else:
                        break
            if main_menu == "remove node":
                all_hosts = [r[0] for r in self.cur.execute('SELECT name FROM hosts').fetchall()]
                all_hosts.append('abort')
                while True:
                    host = cli_ui.ask_choice("Select an option", choices=all_hosts, sort=False)
                    if host == "abort":
                        break
                    if host:
                        host_confirmation = cli_ui.ask_string("Please enter hostname to confirm '" + host + "'")
                        if host_confirmation:
                            if host_confirmation == host:
                                params = (host, )
                                query = """DELETE FROM hosts WHERE name=?"""
                                self.cur.execute(query, params)
                                self.con.commit()
                                break
                            else:
                                cli_ui.info("hostnames don't match, aborting")
            if main_menu == "export all configs":
                config_path = 'wgman1ton_configs'
                if os.path.isdir(config_path):
                    shutil.rmtree(config_path, ignore_errors=False, onerror=None)
                os.mkdir(config_path, mode=0o700)

                hostname = self.cur.execute('SELECT value FROM settings WHERE key = "hostname"').fetchall()[0][0]
                host_ip = self.cur.execute('SELECT value FROM settings WHERE key = "ip"').fetchall()[0][0]
                mask = self.cur.execute('SELECT value FROM settings WHERE key = "ip_mask"').fetchall()[0][0]
                listen_port = self.cur.execute('SELECT value FROM settings WHERE key = "listen_port"').fetchall()[0][0]
                persistent_keepalive = self.cur.execute('SELECT value FROM settings WHERE key = "persistent_keepalive"').fetchall()[0][0]
                host_private_key = self.cur.execute('SELECT value FROM settings WHERE key = "host_private_key"').fetchall()[0][0]
                host_public_key = self.cur.execute('SELECT value FROM settings WHERE key = "host_public_key"').fetchall()[0][0]

                if not os.path.isdir(os.path.join(config_path, hostname)):
                    os.mkdir(os.path.join(config_path, hostname), mode=0o700)

                host_string = "[Interface]\n"
                host_string += "PrivateKey = " + host_private_key + "\n"
                host_string += "Address = " + host_ip + "/" + mask + "\n"
                host_string += "ListenPort = " + listen_port + "\n"
                host_string += "MTU = 1380\n"
                host_string += "\n"

                Path(os.path.join(config_path, "hosts")).touch(mode=0o600, exist_ok=True)
                with open(os.path.join(config_path, "hosts"), "w") as hosts:
                    hosts.write(host_ip + "\t" + hostname + "\n")

                    for client in self.cur.execute('SELECT name, ip, private_key, public_key FROM hosts').fetchall():
                        if not os.path.isdir(os.path.join(config_path, client[0])):
                            os.mkdir(os.path.join(config_path, client[0]), mode=0o700)
                        client_string = "[Interface]\n"
                        client_string += "PrivateKey = " + client[2] + "\n"
                        client_string += "Address = " + client[1] + "/32\n"
                        client_string += "MTU = 1380\n"
                        client_string += "\n"
                        client_string += "[Peer]\n"
                        client_string += "PublicKey = " + host_public_key + "\n"
                        client_string += "AllowedIPs = " + ipaddress.ip_network(host_ip+"/"+mask, False).with_prefixlen + "\n"
                        client_string += "Endpoint = " + hostname + ":" + listen_port + "\n"
                        client_string += "PersistentKeepalive = " + persistent_keepalive + "\n"
                        Path(os.path.join(config_path, client[0], "wg0.conf")).touch(mode=0o600, exist_ok=True)
                        with open(os.path.join(config_path, client[0], "wg0.conf"), "w") as client_config:
                            client_config.write(client_string)
                            client_config.close()
                            img = qrcode.make(client_string)
                            Path(os.path.join(config_path, client[0], "qr.png")).touch(mode=0o600, exist_ok=True)
                            img.save(os.path.join(config_path, client[0], "qr.png"))

                            host_string += "[Peer]\n"
                            host_string += "PublicKey = " + client[3] + "\n"
                            host_string += "AllowedIPs = " + client[1] + "/32\n"
                            host_string += "\n"

                            hosts.write(client[1] + "\t" + client[0] + "\n")
                    hosts.close()
                Path(os.path.join(config_path, hostname, "wg0.conf")).touch(mode=0o600, exist_ok=True)
                with open(os.path.join(config_path, hostname, "wg0.conf"), "w") as host_config:
                    host_config.write(host_string)
                    host_config.close()
            if main_menu == "display qr-code for node":
                all_hosts = [r[0] for r in self.cur.execute('SELECT name FROM hosts').fetchall()]
                host = cli_ui.ask_choice("Select an option", choices=all_hosts)
                if host:
                    host_ip = self.cur.execute('SELECT value FROM settings WHERE key = "ip"').fetchall()[0][0]
                    mask = self.cur.execute('SELECT value FROM settings WHERE key = "ip_mask"').fetchall()[0][0]
                    hostname = self.cur.execute('SELECT value FROM settings WHERE key = "hostname"').fetchall()[0][0]
                    listen_port = self.cur.execute('SELECT value FROM settings WHERE key = "listen_port"').fetchall()[0][0]
                    persistent_keepalive = self.cur.execute('SELECT value FROM settings WHERE key = "persistent_keepalive"').fetchall()[0][0]
                    host_public_key = self.cur.execute('SELECT value FROM settings WHERE key = "host_public_key"').fetchall()[0][0]

                    params = (host, )
                    client = self.cur.execute('SELECT name, ip, private_key, public_key FROM hosts WHERE name = ?', params).fetchall()[0]
                    client_string = "[Interface]\n"
                    client_string += "PrivateKey = " + client[2] + "\n"
                    client_string += "Address = " + client[1] + "/32\n"
                    client_string += "MTU = 1380\n"
                    client_string += "\n"
                    client_string += "[Peer]\n"
                    client_string += "PublicKey = " + host_public_key + "\n"
                    client_string += "AllowedIPs = " + ipaddress.ip_network(host_ip + "/" + mask, False).with_prefixlen + "\n"
                    client_string += "Endpoint = " + hostname + ":" + listen_port + "\n"
                    client_string += "PersistentKeepalive = " + persistent_keepalive + "\n"
                    print(client_string)
                    qr = qrcode.QRCode()
                    qr.add_data(client_string)
                    f = io.StringIO()
                    qr.print_ascii(out=f)
                    f.seek(0)
                    qr_text = f.read()
                    if darkdetect.isDark():
                        qr_text = qr_text.translate(str.maketrans({'▀': '▄', '▄': '▀', '█': ' ', ' ': '█'}))
                    print(qr_text)
            if main_menu == "exit":
                break

        self.con.close()

    def get_unused_ip(self):
        while True:
            mask = self.cur.execute('SELECT value FROM settings WHERE key = "ip_mask"').fetchall()[0][0]
            host_ip = self.cur.execute('SELECT value FROM settings WHERE key = "ip"').fetchall()[0][0]
            ips = [r[0] for r in self.cur.execute('SELECT ip FROM hosts').fetchall()]
            ips.append(host_ip)
            network = ipaddress.ip_network(host_ip+"/"+mask, False)
            rand = random.randint(0, pow(2, (32 - int(mask)) - 1))
            new_ip = str(network[rand])
            if new_ip not in ips:
                print(new_ip)
                return new_ip


