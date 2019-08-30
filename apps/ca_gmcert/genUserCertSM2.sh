#!/bin/sh

CURTIME=`date +"%Y%m%d-%H%M%S"`


############################ HERE ############################ 
TEST_CLIENT_FILE=104@192.168.1.9
TEST_CLIENT_DN="/C=CN/ST=BJ/L=HaiDian/O=SSL TEST ORG/OU=DEV UNIT/CN=$TEST_CLIENT_FILE"
TEST_CLIENT_ENC_FILE="$TEST_CLIENT_FILE"_enc
TEST_CLIENT_ENC_DN="/C=CN/ST=BJ/L=HaiDian/O=SSL TEST ORG/OU=DEV UNIT/CN=$TEST_CLIENT_ENC_FILE"
############################################################## 

# For a list of supported curves, use "apps/openssl ecparam -list_curves".

# Path to the openssl distribution
OPENSSL_DIR=.
# Path to the openssl program
OPENSSL_CMD=openssl_tassl
# Option to find configuration file
OPENSSL_CNF="-config ./openssl.cnf"
# Directory where certificates are stored
CA_DIR=./caCerts
CERTSTOTAL_DIR=./userCerts
CERTS_DIR=$CERTSTOTAL_DIR/"$TEST_CLIENT_FILE"_$CURTIME
# Directory where private key files are stored
KEYS_DIR=$CERTS_DIR
# Directory where combo files (containing a certificate and corresponding
# private key together) are stored
COMBO_DIR=$CERTS_DIR
# cat command
CAT=/bin/cat
# rm command
RM=/bin/rm
# mkdir command
MKDIR=/bin/mkdir
# The certificate will expire these many days after the issue date.
DAYS=1500
TEST_CA_CURVE=SM2
TEST_CA_FILE=CA
 
TEST_CLIENT_CURVE=SM2


# Generating an EC certificate involves the following main steps
# 1. Generating curve parameters (if needed)
# 2. Generating a certificate request
# 3. Signing the certificate request 
# 4. [Optional] One can combine the cert and private key into a single
#    file and also delete the certificate request
  
$MKDIR -p $CERTSTOTAL_DIR
$MKDIR -p $CERTS_DIR
$MKDIR -p $KEYS_DIR
$MKDIR -p $COMBO_DIR

echo "GENERATING A TEST CLIENT CERTIFICATE (on elliptic curve $TEST_CLIENT_CURVE)"
echo "=========================================================================="
# Generate a new certificate request in $TEST_CLIENT_FILE.req.pem. A 
# new ecdsa (actually ECC) key pair is generated on the parameters in
# $TEST_CLIENT_CURVE.pem and the private key is saved in 
# $TEST_CLIENT_FILE.key.pem
# WARNING: By using the -nodes option, we force the private key to be 
# stored in the clear (rather than encrypted with a password).
$OPENSSL_CMD req $OPENSSL_CNF -nodes -subj "$TEST_CLIENT_DN" \
	     -keyout $KEYS_DIR/$TEST_CLIENT_FILE.key.pem \
	     -newkey ec:$TEST_CLIENT_CURVE.pem -new \
	     -out $CERTS_DIR/$TEST_CLIENT_FILE.req.pem

# Sign the certificate request in $TEST_CLIENT_FILE.req.pem using the
# CA certificate in $TEST_CA_FILE.cert.pem and the CA private key in
# $TEST_CA_FILE.key.pem. Since we do not have an existing serial number
# file for this CA, create one. Make the certificate valid for $DAYS days
# from the time of signing. The certificate is written into 
# $TEST_CLIENT_FILE.cert.pem
$OPENSSL_CMD x509 -req -days $DAYS \
    -in $CERTS_DIR/$TEST_CLIENT_FILE.req.pem \
    -CA $CA_DIR/$TEST_CA_FILE.cert.pem \
    -CAkey $CA_DIR/$TEST_CA_FILE.key.pem \
	-extfile $OPENSSL_DIR/openssl.cnf \
	-extensions v3_req \
    -out $CERTS_DIR/$TEST_CLIENT_FILE.cert.pem -CAcreateserial

# Display the certificate 
$OPENSSL_CMD x509 -in $CERTS_DIR/$TEST_CLIENT_FILE.cert.pem -text

# Place the certificate and key in a common file
$OPENSSL_CMD x509 -in $CERTS_DIR/$TEST_CLIENT_FILE.cert.pem -issuer -subject \
	 > $COMBO_DIR/$TEST_CLIENT_FILE.pfx
$CAT $KEYS_DIR/$TEST_CLIENT_FILE.key.pem >> $COMBO_DIR/$TEST_CLIENT_FILE.pfx

# Remove the cert request file (no longer needed)
$RM $CERTS_DIR/$TEST_CLIENT_FILE.req.pem


echo "	GENERATING A TEST CLIENT ENCRYPT CERTIFICATE (on elliptic curve $TEST_CLIENT_CURVE)"
echo "	==================================================================================="
# Generate a new certificate request in $TEST_CLIENT_FILE.req.pem. A 
# new ecdsa (actually ECC) key pair is generated on the parameters in
# $TEST_CLIENT_CURVE.pem and the private key is saved in 
# $TEST_CLIENT_FILE.key.pem
# WARNING: By using the -nodes option, we force the private key to be 
# stored in the clear (rather than encrypted with a password).
$OPENSSL_CMD req $OPENSSL_CNF -nodes -subj "$TEST_CLIENT_ENC_DN" \
	     -keyout $KEYS_DIR/$TEST_CLIENT_ENC_FILE.key.pem \
	     -newkey ec:$TEST_CLIENT_CURVE.pem -new \
	     -out $CERTS_DIR/$TEST_CLIENT_ENC_FILE.req.pem

# Sign the certificate request in $TEST_CLIENT_FILE.req.pem using the
# CA certificate in $TEST_CA_FILE.cert.pem and the CA private key in
# $TEST_CA_FILE.key.pem. Since we do not have an existing serial number
# file for this CA, create one. Make the certificate valid for $DAYS days
# from the time of signing. The certificate is written into 
# $TEST_CLIENT_FILE.cert.pem
$OPENSSL_CMD x509 -req -days $DAYS \
    -in $CERTS_DIR/$TEST_CLIENT_ENC_FILE.req.pem \
    -CA $CA_DIR/$TEST_CA_FILE.cert.pem \
    -CAkey $CA_DIR/$TEST_CA_FILE.key.pem \
	-extfile $OPENSSL_DIR/openssl.cnf \
	-extensions v3enc_req \
    -out $CERTS_DIR/$TEST_CLIENT_ENC_FILE.cert.pem -CAcreateserial

# Display the certificate 
$OPENSSL_CMD x509 -in $CERTS_DIR/$TEST_CLIENT_ENC_FILE.cert.pem -text

# Place the certificate and key in a common file
$OPENSSL_CMD x509 -in $CERTS_DIR/$TEST_CLIENT_ENC_FILE.cert.pem -issuer -subject \
	 > $COMBO_DIR/$TEST_CLIENT_ENC_FILE.pfx
$CAT $KEYS_DIR/$TEST_CLIENT_ENC_FILE.key.pem >> $COMBO_DIR/$TEST_CLIENT_ENC_FILE.pfx

# Remove the cert request file (no longer needed)
$RM $CERTS_DIR/$TEST_CLIENT_ENC_FILE.req.pem


