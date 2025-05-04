

# sudo apt install -y i2c-tools
# i2cdetect -y 1

# Load i2c-dev kernel module now
sudo modprobe i2c-dev

# Add i2c-dev to auto-load on boot
echo "i2c-dev" | sudo tee -a /etc/modules

# Enable I2C in /boot/config.txt
sudo sed -i '/^#dtparam=i2c_arm=on/s/^#//' /boot/config.txt
grep -q '^dtparam=i2c_arm=on' /boot/config.txt || echo 'dtparam=i2c_arm=on' | sudo tee -a /boot/config.txt

# Reboot for changes to take effect
echo "✅ I2C enabled. Rebooting..."
sudo reboot
