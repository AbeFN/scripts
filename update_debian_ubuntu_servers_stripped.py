import subprocess
import sys
import time
import getpass

# List of servers: (Friendly name, SSH target)
servers = [
    ('SERVERNAME', 'user@192.168.1.11'),
    ('SERVERNAME', 'user@192.168.1.12'),
    ('SERVERNAME', 'user@192.168.1.13'),
    ('SERVERNAME', 'user@192.168.1.14'),
    ('SERVERNAME', 'user@192.168.1.15'),
    ('SERVERNAME', 'user@192.168.1.16'),
    ('SERVERNAME', 'user@192.168.1.17'),
]

sudo_password = getpass.getpass("Enter your sudo password: ")

remote_cmd = '''
echo "{pwd}" | sudo -S -p '' DEBIAN_FRONTEND=noninteractive apt update -qq && \
echo "System packages updated." && \
echo "{pwd}" | sudo -S -p '' DEBIAN_FRONTEND=noninteractive apt upgrade -y -qq && \
echo "System packages upgraded." && \
echo "{pwd}" | sudo -S -p '' DEBIAN_FRONTEND=noninteractive apt autoremove -y -qq && \
echo "Unused packages removed." && \
echo "{pwd}" | sudo -S -p '' DEBIAN_FRONTEND=noninteractive apt autoclean -qq && \
echo "Package cache cleaned."
'''.format(pwd=sudo_password)

def run_update(server_name, ssh_target):
    print(f'\n{"="*60}')
    print(f'Updating server: {server_name} ({ssh_target})')
    print(f'{"="*60}')

    try:
        process = subprocess.Popen(
            ['ssh', '-o', 'BatchMode=yes', ssh_target, remote_cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        spinner = ['|', '/', '-', '\\']
        idx = 0
        while process.poll() is None:
            sys.stdout.write(f'\rUpdating... {spinner[idx % len(spinner)]}')
            sys.stdout.flush()
            time.sleep(0.2)
            idx += 1

        stdout, stderr = process.communicate()
        sys.stdout.write('\rUpdate completed.            \n')

        if process.returncode == 0:
            print(f'✅ {server_name} successfully updated.')
        else:
            print(f'❌ {server_name} failed with return code {process.returncode}')
            print(f'[stderr]: {stderr.strip()}')

    except subprocess.TimeoutExpired:
        print(f'❌ Timeout updating {server_name}')
    except Exception as e:
        print(f'❌ Error updating {server_name}: {e}')

def main():
    for name, target in servers:
        run_update(name, target)

if __name__ == '__main__':
    main()
