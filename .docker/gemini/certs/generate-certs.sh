#!/bin/bash
# Generate TLS certificates for molly-brown gemini server
# Run this script before starting the Docker container for the first time

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Generating TLS certificates for gemini server..."

cd "$SCRIPT_DIR"

# Generate certificate with SANs using openssl.cnf
openssl req -x509 -newkey rsa:2048 \
    -keyout key.pem \
    -out cert.pem \
    -days 365 \
    -nodes \
    -config openssl.cnf \
    -extensions v3_req

echo ""
echo "✓ Certificates generated successfully!"
echo ""
echo "Generated files:"
echo "  - cert.pem (certificate)"
echo "  - key.pem (private key)"
echo ""
echo "Subject Alternative Names:"
openssl x509 -in cert.pem -text -noout | grep -A 3 "Subject Alternative Name"
echo ""
echo "You can now start the gemini Docker container:"
echo "  docker compose -f docker-compose.gemini.yml up -d"
