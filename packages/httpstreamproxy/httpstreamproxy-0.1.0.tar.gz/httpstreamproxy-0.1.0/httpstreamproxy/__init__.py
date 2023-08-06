from httpstreamproxy.httpproxy import run_server
from httpstreamproxy.app import App
from string import Template


PACKAGENAME = 'httpstreamproxy'
ENTRY_POINT = "httpproxy"
DESCRIPTION = "A http stream proxy"



UNIT_TEMPLATE = Template('''
[Unit]
Description=$packagename
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=$entrypoint --command listen --port $port --target_url $target_url --verify $verify 
SyslogIdentifier=$packagename
StandardOutput=syslog
StandardError=syslog
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
''')



class InternetApp(App):

    def do_add_argument(self, parser):
        parser.add_argument('--target_url', metavar='target_url', required=False, type=str, help='the target url to proxy')
        parser.add_argument('--verify', metavar='verify', required=False, type=str, default="True", help='True, if the (certificate of the) proxied connection should be verified')

    def do_additional_listen_example_params(self):
        return '--target_uri http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4 ---verify "True"'


    def do_process_command(self, command:str, port: int, verbose: bool, args) -> bool:
        if command == 'listen':
            bool_verify = True if args.verify == 'True' else False
            run_server(port, target_url=args.target_url, verify=bool_verify)
            return True
        elif args.command == 'register':
            print("register " + self.packagename + " on port " + str(args.port))
            unit = UNIT_TEMPLATE.substitute(packagename=self.packagename, entrypoint=self.entrypoint, port=port, verify=args.verify, target_url=args.target_url, verbose=verbose)
            self.unit.register(port, unit)
            return True
        else:
            return False

def main():
    InternetApp(PACKAGENAME, ENTRY_POINT, DESCRIPTION).handle_command()


if __name__ == '__main__':
    main()

