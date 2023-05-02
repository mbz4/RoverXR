#!/bin/bash
echo "Installing autostart service..."
echo "This needs to be run from the install directory"
loginctl enable-linger "$USER"
# Copy the service file to the user's systemd directory
mkdir -p "$HOME/.config/systemd/user"
cp autostart.service "$HOME/.config/systemd/user/"

# Reload the systemd configuration and start the service
systemctl --user daemon-reload
# Enable the service to start automatically at login
systemctl --user enable autostart.service
systemctl --user start autostart.service