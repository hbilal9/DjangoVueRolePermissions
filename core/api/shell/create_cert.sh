#!/bin/bash

# Generate user certificate
generate_user_cert() {
    USERNAME=$1
    cd /etc/openvpn/easy-rsa  # Ensure correct directory path
    
    # Remove existing request files if they exist
    sudo rm -f pki/reqs/$USERNAME.req
    sudo rm -f pki/private/$USERNAME.key
    sudo rm -f pki/issued/$USERNAME.crt
    
    sudo ./easyrsa --batch build-client-full $USERNAME nopass
    
    # Ensure the clients directory exists
    sudo mkdir -p /etc/openvpn/clients
    
    sudo cp pki/private/$USERNAME.key /etc/openvpn/clients/
    sudo cp pki/issued/$USERNAME.crt /etc/openvpn/clients/
    sudo cp pki/ca.crt /etc/openvpn/clients/
    sudo cp /etc/openvpn/clients/ta.key /etc/openvpn/clients/
    
    # Create a group for OpenVPN certificates if it doesn't exist
    sudo groupadd -f openvpn-cert
    
    # Add the current user and www-data to the group
    sudo usermod -a -G openvpn-cert www-data
    sudo usermod -a -G openvpn-cert $(whoami)
    
    # Set proper ownership and permissions
    sudo chown ubuntu:www-data /etc/openvpn/clients/$USERNAME.key
    sudo chown ubuntu:www-data /etc/openvpn/clients/$USERNAME.crt
    sudo chown ubuntu:www-data /etc/openvpn/clients/ca.crt
    sudo chown ubuntu:www-data /etc/openvpn/clients/ta.key
    
    # Set proper file permissions (group readable)
    sudo chmod 640 /etc/openvpn/clients/$USERNAME.key
    sudo chmod 640 /etc/openvpn/clients/$USERNAME.crt
    sudo chmod 640 /etc/openvpn/clients/ca.crt
    sudo chmod 640 /etc/openvpn/clients/ta.key
    
    # Set proper directory permissions
    sudo chmod 750 /etc/openvpn/clients
}

# Call the function with the username
generate_user_cert "$1"
