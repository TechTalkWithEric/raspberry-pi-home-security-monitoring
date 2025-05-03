#!/bin/bash
set -e

echo "🔧 Enabling I2C and GPIO Expander Support..."

# Load i2c kernel module immediately
sudo modprobe i2c-dev

# Ensure modules are loaded on boot
grep -qxF "i2c-dev" /etc/modules || echo "i2c-dev" | sudo tee -a /etc/modules

# Enable I2C in /boot/config.txt
if ! grep -q "^dtparam=i2c_arm=on" /boot/config.txt; then
  echo "dtparam=i2c_arm=on" | sudo tee -a /boot/config.txt
fi

# 📦 Install i2c and GPIO utilities
echo "📦 Installing packages..."
sudo apt-get update
sudo apt-get install -y \
  i2c-tools \
  python3-pip \
  python3-smbus \



sudo apt remove pigpio
cd ~
git clone https://github.com/joan2937/pigpio.git
cd pigpio
make
sudo make install
sudo pigpiod
sudo systemctl status pigpiod
sudo apt remove lgpio python3-lgpio
sudo apt remove python3-lgpio
sudo apt remove pigpio 
sudo apt remove python3-pigpio
sudo apt install lgpio python3-lgpio


# 📦 Install Python libraries for MCP23017
echo "📦 Installing Python libraries..."
# pip3 install --upgrade pip
# pip3 install adafruit-circuitpython-mcp230xx

# Enable pigpiod daemon to auto-start (if using pigpio)
sudo systemctl enable pigpiod
sudo systemctl start pigpiod

# Confirm I2C device
echo "🔍 Scanning I2C bus (should see 0x20 for MCP23017)..."
i2cdetect -y 1

# Final step
read -p "✅ All done. Reboot now to apply kernel module changes? [y/N]: " confirm
if [[ "$confirm" =~ ^[Yy]$ ]]; then
  echo "♻️ Rebooting..."
  sudo reboot
else
  echo "🚨 Reboot manually to complete I2C setup."
fi
