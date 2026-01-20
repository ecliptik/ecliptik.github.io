# Gemini TLS Certificates

This directory contains TLS certificates for the molly-brown gemini server used in local development.

## Security Notice

**The certificate files (`cert.pem` and `key.pem`) are NOT committed to git for security reasons.**

You must generate them locally before starting the Docker container.

## Generating Certificates

### Quick Start

```bash
# From the repository root:
./smallweb/gemini/config/certs/generate-certs.sh
```

### Manual Generation

```bash
cd smallweb/gemini/config/certs
openssl req -x509 -newkey rsa:2048 \
    -keyout key.pem \
    -out cert.pem \
    -days 365 \
    -nodes \
    -config openssl.cnf \
    -extensions v3_req
```

## Certificate Details

The certificates are configured with Subject Alternative Names (SANs) for:
- `jezebel` (Tailscale hostname)
- `jezebel.hale-gopher.ts.net` (Tailscale FQDN)
- `localhost` (local testing)
- `*.localhost` (local wildcard)
- `127.0.0.1` (IPv4 loopback)
- `::1` (IPv6 loopback)

These SANs allow the gemini server to work on:
- Local machine: `gemini://localhost:1965/`
- Tailscale network: `gemini://jezebel:1965/`
- Tailscale FQDN: `gemini://jezebel.hale-gopher.ts.net:1965/`

## Files

- `openssl.cnf` - OpenSSL configuration with SAN definitions (committed)
- `generate-certs.sh` - Certificate generation script (committed)
- `cert.pem` - TLS certificate (NOT committed, generated locally)
- `key.pem` - Private key (NOT committed, generated locally)
- `README.md` - This file (committed)

## Expiration

Self-signed certificates are valid for 365 days. Regenerate them annually or when needed.

## Verifying Certificates

```bash
# View certificate details
openssl x509 -in cert.pem -text -noout

# Check SANs specifically
openssl x509 -in cert.pem -text -noout | grep -A 3 "Subject Alternative Name"
```
