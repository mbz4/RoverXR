#!/bin/bash
echo "Installing autostart service..."
echo "$PWD"
echo "This needs to be run from the install directory: edu_teleop_demo/Blueprints/Install"
loginctl enable-linger "$USER"
mkdir -p "$HOME/.config/systemd/user"
cp autostart.service "$HOME/.config/systemd/user/" # Copy the service file to the user's systemd directory
systemctl --user daemon-reload # Reload the systemd configuration and start the service
systemctl --user enable autostart.service # Enable the service to start automatically at login
systemctl --user start autostart.service