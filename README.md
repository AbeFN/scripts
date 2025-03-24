# scripts

A collection of handy scripts that I have created.

## Scripts

### `update_debian_ubuntu_servers_stripped.py`
Remotely connects to a list of Debian/Ubuntu servers one-by-one over SSH and updates packages.  
- Supports `sudo` with a provided password
- Displays status as it updates and upgrades
- Minimal output, user-friendly spinner
- Requires Python 3

**Usage:**

```bash
python3 update_debian_ubuntu_servers_stripped.py
