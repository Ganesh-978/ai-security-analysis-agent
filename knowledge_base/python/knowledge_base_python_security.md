# Python Security — Detailed RAG Knowledge Base

> **Primary official source:** https://docs.python.org/3/library/security_warnings.html
> **Purpose:** Detailed RAG knowledge for the AI Code Review & Security Analysis Agent.

---

# 1. Purpose
This knowledge base serves as a foundational resource for the AI Code Review & Security Analysis Agent, specifically tailored for Python applications. Its primary purpose is to equip the agent with comprehensive understanding of common security vulnerabilities, best practices, and quality standards pertinent to Python development. By leveraging this detailed documentation, the AI agent will be able to accurately identify potential security flaws, suggest robust remediation strategies, and provide context-rich explanations during the code review process. The goal is to foster a proactive security posture, enabling developers to build more resilient and trustworthy software from the outset, reducing the attack surface, and mitigating risks associated with insecure coding patterns. This document aims to standardize the agent's security analysis, ensuring consistency, depth, and relevance in its findings, ultimately enhancing the overall security and quality of Python projects.

```text
Key Review Checks:
- Understand the AI agent's role in security analysis.
- Identify the scope of Python security concerns covered.
- Ensure the agent's output aligns with proactive security principles.
- Verify the agent's ability to provide actionable remediation.
- Confirm the agent's adherence to documented best practices.
```

```python
# Poor: No explicit security considerations in project setup
class InsecureApp:
    def __init__(self):
        print("Application initialized without specific security guidelines.")
        # No explicit security configurations or checks are defined here.
        # This approach assumes security will be handled implicitly or later,
        # which often leads to vulnerabilities.

# Preferred: Explicitly state security goals and integrate security from the start
class SecureApp:
    def __init__(self):
        print("Application initialized with security as a core principle.")
        self.security_policy = {
            "input_validation": True,
            "least_privilege": True,
            "secure_defaults": True,
            "logging_enabled": True
        }
        # Security considerations are explicitly part of the design and initialization.
        # This sets a clear expectation for secure coding practices throughout the project.
```

Assistant behavior guidance:
When reviewing code, the agent should always refer to this knowledge base to identify potential security weaknesses. If a pattern deviates from the documented secure practices, the agent should flag it, explain the security risk, and provide a reference to the relevant section in this document for detailed context and remediation steps. Emphasize the importance of integrating security early in the development lifecycle.

---

# 2. Trust boundaries
Trust boundaries are conceptual lines within an application or system architecture that separate components or data based on their level of trustworthiness. Data originating from outside a trust boundary (e.g., user input from a web browser, data from an external API, files uploaded by users) is considered untrusted and must be rigorously validated, sanitized, and authorized before being processed or allowed to cross into a more trusted zone. Conversely, data generated within a trusted boundary (e.g., internal configuration, database records after validation) can be treated with a higher degree of confidence, though internal validation is still prudent. Failing to properly define and enforce trust boundaries is a common root cause of many security vulnerabilities, as it allows malicious or malformed data to bypass security controls and interact with sensitive internal components, leading to issues like injection attacks, unauthorized access, or data corruption. Understanding and meticulously managing trust boundaries is fundamental to designing secure systems.

```text
Key Review Checks:
- Identify all external data sources and their entry points.
- Map data flow across different components and services.
- Verify that all data crossing a trust boundary is validated.
- Check for proper authorization checks at boundary crossings.
- Ensure sensitive internal data does not flow out without sanitization.
- Look for clear separation of concerns between trusted and untrusted zones.
```

```python
# Vulnerable: Trusting user input without proper boundary enforcement
def process_user_data_vulnerable(user_input):
    # User input is directly used to construct a file path within a trusted zone.
    # This bypasses the trust boundary without validation.
    file_path = f"/app/data/{user_input}.txt"
    with open(file_path, 'w') as f:
        f.write("User data processed.")
    print(f"File created at {file_path}")

# Preferred: Enforcing trust boundaries with validation
import os

def process_user_data_secure(user_input):
    # Define a trusted base directory.
    base_dir = "/app/data"
    # Validate user input against an allowlist or strict pattern.
    if not user_input.isalnum(): # Example: Only alphanumeric filenames allowed
        print("Invalid input: Filename must be alphanumeric.")
        return

    # Construct the path safely, ensuring it stays within the trusted base directory.
    # os.path.join handles path segments correctly, and realpath resolves '..'
    # A more robust check would involve comparing the resolved path with the base_dir.
    safe_filename = user_input + ".txt"
    potential_path = os.path.join(base_dir, safe_filename)

    # Ensure the resolved path is indeed within the base directory to prevent path traversal.
    # This is a critical step in enforcing the trust boundary.
    abs_base_dir = os.path.abspath(base_dir)
    abs_potential_path = os.path.abspath(potential_path)

    if not abs_potential_path.startswith(abs_base_dir):
        print("Security alert: Attempted path traversal detected.")
        return

    with open(abs_potential_path, 'w') as f:
        f.write("User data processed securely.")
    print(f"File created at {abs_potential_path}")

# Example usage:
# process_user_data_vulnerable("../../etc/passwd") # Vulnerable to path traversal
# process_user_data_secure("report123") # Secure
# process_user_data_secure("../../etc/passwd") # Blocked by validation
```

Assistant behavior guidance:
The agent should identify areas where data from untrusted sources is used directly without validation or sanitization, especially when crossing into sensitive operations (e.g., file system access, database queries, command execution). Flag these instances as trust boundary violations, explain the potential impact (e.g., path traversal, injection), and recommend implementing strict input validation and sanitization at the boundary.

---

# 3. Input validation
Input validation is a critical security control that ensures all data received by an application conforms to expected formats, types, and ranges before it is processed. This principle, often summarized as "never trust user input," applies to all data sources, including user-supplied forms, URL parameters, HTTP headers, cookies, API payloads, and even data from other internal systems if their trust level is not absolute. Without proper validation, an application is susceptible to a wide array of attacks, such as injection (SQL, command, XSS), buffer overflows, logic bombs, and denial-of-service. Validation should be performed as early as possible in the request lifecycle, ideally at the application's entry points, and should be comprehensive, checking for data type, length, format, range, and semantic correctness. Relying solely on client-side validation is insufficient, as it can be easily bypassed by an attacker; server-side validation is mandatory.

```text
Key Review Checks:
- Identify all points where external data enters the application.
- Verify that every input parameter is explicitly validated.
- Check for validation of data type, length, format (regex), and range.
- Ensure semantic validation (e.g., valid email domain, existing user ID).
- Look for both client-side and mandatory server-side validation.
- Confirm that validation errors are handled gracefully and securely.
- Check for validation of HTTP headers, cookies, and file uploads.
```

```python
# Vulnerable: Missing or insufficient input validation
def get_user_profile_vulnerable(user_id):
    # User ID is directly used in a database query without validation.
    # An attacker could inject SQL here (e.g., "1 OR 1=1").
    query = f"SELECT * FROM users WHERE id = {user_id}"
    print(f"Executing query: {query}")
    # Assume database execution here
    return {"message": "Profile retrieved (potentially insecurely)"}

def create_product_vulnerable(name, price):
    # No validation on name or price.
    # Name could be an XSS payload, price could be negative or non-numeric.
    if not name or not price:
        return "Error: Name and price are required."
    print(f"Product '{name}' created with price {price}.")
    return {"message": f"Product '{name}' created."}

# Preferred: Robust input validation
import re

def get_user_profile_secure(user_id_str):
    # Validate user_id_str to ensure it's a positive integer.
    if not user_id_str.isdigit() or int(user_id_str) <= 0:
        print("Validation Error: User ID must be a positive integer.")
        return {"error": "Invalid User ID"}
    
    user_id = int(user_id_str)
    # Now use the validated integer in a parameterized query (best practice).
    # For demonstration, we'll just print the safe query.
    query = "SELECT * FROM users WHERE id = %s"
    print(f"Executing secure query: {query} with parameter {user_id}")
    # Assume database execution with parameterized query here
    return {"message": "Profile retrieved securely"}

def create_product_secure(name, price_str):
    # Validate product name: non-empty, max length, alphanumeric with spaces/hyphens.
    if not name or not (1 <= len(name) <= 100) or not re.match(r"^[a-zA-Z0-9\s\-]+$", name):
        print("Validation Error: Invalid product name.")
        return {"error": "Invalid product name"}

    # Validate price: must be a positive number.
    try:
        price = float(price_str)
        if price <= 0:
            raise ValueError
    except ValueError:
        print("Validation Error: Price must be a positive number.")
        return {"error": "Invalid price"}
    
    print(f"Product '{name}' created with price {price}.")
    return {"message": f"Product '{name}' created securely."}

# Example usage:
# get_user_profile_vulnerable("1 OR 1=1")
# get_user_profile_secure("1")
# get_user_profile_secure("invalid_id")

# create_product_vulnerable("<script>alert('XSS')</script>", "-100")
# create_product_secure("Secure Product Name", "99.99")
# create_product_secure("Product Name!", "invalid")
```

Assistant behavior guidance:
The agent should flag any function or endpoint that accepts external input (e.g., from request parameters, body, headers) and uses it without explicit, robust validation. Clearly state the type of validation missing (e.g., type, length, format) and the potential vulnerability (e.g., SQL injection, XSS, DoS). Recommend implementing comprehensive server-side validation using appropriate data types, regular expressions, and range checks.

---

# 4. Allowlist validation
Allowlist (or whitelist) validation is a security best practice that involves explicitly defining and permitting only known-good inputs, rejecting everything else by default. This approach is inherently more secure than denylist (or blacklist) validation, which attempts to block known-bad inputs. Denylists are notoriously difficult to maintain and are often incomplete, as attackers can frequently find new ways to bypass them by crafting novel malicious payloads that are not on the list. In contrast, an allowlist provides a strong security posture by strictly controlling what is allowed, making it much harder for attackers to introduce unexpected or malicious data. This method is particularly effective for validating file extensions, URL parameters, character sets, and specific values in dropdowns or checkboxes. When implementing allowlist validation, it's crucial to define the allowed set as narrowly as possible to maximize security.

```text
Key Review Checks:
- Identify all validation logic for user-supplied values.
- Check if denylist (blacklist) patterns are used (e.g., blocking specific characters).
- Verify if allowlist (whitelist) patterns are implemented (e.g., allowing only alphanumeric).
- Look for explicit definitions of allowed values, characters, or formats.
- Ensure that file uploads validate extensions against an allowlist.
- Confirm that URL redirects validate target domains against an allowlist.
- Review regex patterns to ensure they are allowlist-based.
```

```python
# Vulnerable: Denylist validation (easy to bypass)
def validate_filename_denylist(filename):
    # Attempts to block common dangerous characters.
    # This is incomplete and can be bypassed (e.g., using URL encoding, or less common chars).
    bad_chars = ['/', '\\', '..', ';', '&', '|', '`']
    for char in bad_chars:
        if char in filename:
            print(f"Vulnerable: Filename contains blocked character '{char}'.")
            return False
    print(f"Vulnerable: Filename '{filename}' passed denylist validation.")
    return True

# Preferred: Allowlist validation (secure by default)
import re

def validate_filename_allowlist(filename):
    # Allows only alphanumeric characters, hyphens, and underscores.
    # This explicitly defines what is permitted, rejecting everything else.
    if re.match(r"^[a-zA-Z0-9\-_.]+$", filename):
        print(f"Secure: Filename '{filename}' passed allowlist validation.")
        return True
    print(f"Secure: Filename '{filename}' failed allowlist validation (contains disallowed characters).")
    return False

def process_file_vulnerable(filename):
    if validate_filename_denylist(filename):
        print(f"Processing file (vulnerable): {filename}")
    else:
        print("File processing blocked by denylist.")

def process_file_secure(filename):
    if validate_filename_allowlist(filename):
        print(f"Processing file (secure): {filename}")
    else:
        print("File processing blocked by allowlist.")

# Example usage:
# process_file_vulnerable("my_document.txt")
# process_file_vulnerable("my_document;rm -rf /") # Denylist might miss this depending on implementation
# process_file_vulnerable("my_document%2F..%2F..%2Fetc%2Fpasswd") # URL encoded bypass

# process_file_secure("my_document.txt")
# process_file_secure("my_document;rm -rf /") # Blocked
# process_file_secure("my_document%2F..%2F..%2Fetc%2Fpasswd") # Blocked
```

Assistant behavior guidance:
The agent should identify any validation logic that relies on denylists to filter out malicious input. Flag these instances as potentially insecure and explain why denylists are prone to bypasses. Recommend refactoring the validation to use an allowlist approach, specifying exactly what characters, formats, or values are permitted, and rejecting all others by default. Provide examples of robust allowlist regular expressions or explicit value checks.

---

# 5. Schema and type validation
Schema and type validation are crucial for ensuring the integrity and security of structured data inputs, such as JSON, XML, or form data. This form of validation goes beyond simple character checks to verify the overall structure, expected data types for each field, and adherence to predefined constraints (e.g., minimum/maximum length, numeric ranges, enum values). When an application receives complex data, validating its schema and types prevents malformed payloads from reaching business logic, which could otherwise lead to unexpected behavior, application crashes, or even security vulnerabilities like type confusion attacks, logic bypasses, or denial-of-service. Libraries like Pydantic for Python are excellent tools for defining and enforcing schemas, automatically converting data to the correct types and raising errors for invalid inputs. This ensures that the application always operates on well-formed and type-safe data, significantly improving robustness and security.

```text
Key Review Checks:
- Identify endpoints or functions that process structured data (JSON, XML, form data).
- Check for explicit schema definitions (e.g., using Pydantic, Marshmallow, JSON Schema).
- Verify that data types are enforced for each field (e.g., integer, string, boolean).
- Look for validation of field constraints (e.g., min/max values, string length, regex patterns).
- Ensure that nested structures are also validated recursively.
- Confirm that invalid data results in clear, secure error responses.
- Check for the use of robust validation libraries rather than custom, error-prone logic.
```

```python
# Vulnerable: Lack of schema and type validation for JSON input
import json

def process_order_vulnerable(request_body):
    try:
        data = json.loads(request_body)
        # Assuming 'item_id' is an integer and 'quantity' is a positive integer.
        # No explicit type or value validation.
        item_id = data.get('item_id')
        quantity = data.get('quantity')

        # If item_id is not an int, or quantity is negative/zero, this could lead to errors
        # or unexpected behavior downstream (e.g., database errors, negative stock).
        # An attacker could send {"item_id": "DROP TABLE orders;", "quantity": -1}
        print(f"Processing order for item {item_id} with quantity {quantity}")
        return {"status": "Order processed (vulnerable)"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

# Preferred: Robust schema and type validation using Pydantic
from pydantic import BaseModel, Field, ValidationError
from typing import Optional

class OrderItem(BaseModel):
    item_

---

# 29. Message integrity and HMAC

Message integrity is a fundamental security property that ensures data has not been altered or corrupted during transmission or storage by unauthorized entities. Without integrity, a malicious actor could tamper with messages, commands, or data, leading to incorrect application behavior, data corruption, or even system compromise. Cryptographic hash functions, such as SHA-256 or SHA-3, are often used to provide a checksum, but they only guarantee integrity if the hash itself is protected. To protect against active tampering where an attacker can modify both the message and its hash, a Message Authentication Code (MAC) is required. HMAC (Hash-based Message Authentication Code) is a specific type of MAC that uses a cryptographic hash function and a secret key. The key ensures that only parties who know the secret key can generate or verify the HMAC, thus providing both data integrity and data authenticity. This means not only can we verify that the message hasn't changed, but also that it originated from a trusted sender who possesses the secret key. Failing to use HMAC or using it incorrectly (e.g., hardcoding keys, using weak keys, or not verifying the HMAC) can lead to critical vulnerabilities where attackers can forge messages, bypass authorization, or inject malicious data into a system. It is crucial to use robust, randomly generated keys and manage them securely, separate from the data they protect.

```text
Key Review Checks:
- Is message integrity required for this data?
- Is HMAC being used to protect message integrity and authenticity?
- Is a strong, randomly generated secret key used for HMAC?
- Is the secret key managed securely (e.g., environment variable, secret manager) and not hardcoded?
- Is the HMAC correctly generated and verified for all critical messages?
- Are the HMAC algorithm and key length appropriate for the security requirements?
- Is `hmac.compare_digest()` used for constant-time comparison to prevent timing attacks?
```

Vulnerable:
```python
import hashlib

# This is insecure because an attacker can recompute the hash if they modify the message.
# It only provides a checksum, not authenticity or tamper-resistance against an active attacker.
def create_message_checksum(message_data: str) -> str:
    return hashlib.sha256(message_data.encode()).hexdigest()

def verify_message_checksum(message_data: str, received_checksum: str) -> bool:
    return create_message_checksum(message_data) == received_checksum

# Example usage:
data = "user_id=123&action=delete_account"
checksum = create_message_checksum(data)
print(f"Original checksum: {checksum}")

# An attacker modifies the data and recomputes the checksum
modified_data = "user_id=123&action=create_admin"
modified_checksum = create_message_checksum(modified_data)
print(f"Modified checksum: {modified_checksum}")

# The verification would pass, allowing the attacker's forged message
if verify_message_checksum(modified_data, modified_checksum):
    print("Vulnerable: Checksum verification passed for modified data!")
else:
    print("Vulnerable: Checksum verification failed (unexpected).")
```

Secure:
```python
import hmac
import hashlib
import os

# A strong, securely managed secret key is essential.
# NEVER hardcode keys in production code. Use environment variables or a secret manager.
SECRET_KEY = os.getenv("HMAC_SECRET_KEY", "a_very_long_and_random_default_secret_key_for_dev_only_1234567890abcdef")
if SECRET_KEY == "a_very_long_and_random_default_secret_key_for_dev_only_1234567890abcdef":
    print("Warning: Using default HMAC secret key. Ensure a strong, unique key is set in production via HMAC_SECRET_KEY environment variable.")

def create_message_hmac(message_data: str) -> str:
    h = hmac.new(SECRET_KEY.encode(), message_data.encode(), hashlib.sha256)
    return h.hexdigest()

def verify_message_hmac(message_data: str, received_hmac: str) -> bool:
    expected_hmac = create_message_hmac(message_data)
    # Use hmac.compare_digest for constant-time comparison to prevent timing attacks
    return hmac.compare_digest(expected_hmac, received_hmac)

# Example usage:
data = "user_id=123&action=delete_account"
message_hmac = create_message_hmac(data)
print(f"Original HMAC: {message_hmac}")

# Simulate transmission and verification
if verify_message_hmac(data, message_hmac):
    print("Secure: HMAC verification passed for original data.")
else:
    print("Secure: HMAC verification failed for original data (unexpected).")

# An attacker modifies the data but cannot recompute the HMAC without the secret key
modified_data = "user_id=123&action=create_admin"
# Attacker tries to use the original HMAC with modified data
if verify_message_hmac(modified_data, message_hmac):
    print("Vulnerable: HMAC verification passed for modified data (this should not happen).")
else:
    print("Secure: HMAC verification failed for modified data, as expected.")

# If an attacker tries to forge a new HMAC without the key, it will fail
forged_hmac = "deadbeef" * 8 # A random, incorrect HMAC
if verify_message_hmac(modified_data, forged_hmac):
    print("Vulnerable: Forged HMAC verification passed (this should not happen).")
else:
    print("Secure: Forged HMAC verification failed, as expected.")
```

Assistant Behavior Guidance:
The AI should flag any instance where message integrity is critical but only a simple hash (e.g., `hashlib.sha256`) is used without a secret key, or where a custom MAC implementation is used instead of `hmac`. It should also flag hardcoded secret keys or keys retrieved insecurely. The report should explain that simple hashes only provide a checksum and do not protect against active tampering, emphasizing the need for HMAC for both integrity and authenticity. It should recommend using `hmac.new()` with a strong, securely managed key and `hmac.compare_digest()` for verification, providing clear examples of how to implement this securely.

---

# 30. TLS/SSL certificate verification

TLS/SSL certificate verification is a critical security mechanism that ensures the authenticity of the server or client you are communicating with over an encrypted channel. When a client connects to a server using HTTPS, the server presents a digital certificate. The client's role is to verify this certificate to confirm that it is indeed connecting to the intended server and not an imposter (e.g., a man-in-the-middle attacker). This verification process typically involves checking the certificate's validity period, ensuring it is signed by a trusted Certificate Authority (CA), and confirming that the hostname in the certificate matches the hostname being accessed. Disabling certificate verification, often done with `verify=False` in HTTP client libraries like Python's `requests`, completely undermines the security benefits of TLS. It makes the application vulnerable to man-in-the-middle attacks, where an attacker can intercept, read, and modify encrypted traffic without the client detecting anything amiss. This is a common mistake made during development or testing that sometimes makes its way into production, creating a severe security flaw. Always ensure certificate verification is enabled, and if custom certificates are needed (e.g., for internal services with self-signed certs), provide the path to the trusted CA bundle.

```text
Key Review Checks:
- Is `verify=False` explicitly set in any HTTP client requests (e.g., `requests.get`, `httpx.get`)?
- Are custom certificate bundles (CA certificates) correctly specified when needed?
- Is the application communicating with external services over HTTPS without proper verification?
- Are self-signed certificates used in production without a trusted mechanism to verify them?
- Is there any logic that bypasses or weakens standard TLS verification?
```

Vulnerable:
```python
import requests
import warnings

# Suppress InsecureRequestWarning for demonstration purposes.
# In a real application, this warning indicates a problem that needs to be fixed.
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# This code explicitly disables SSL certificate verification, making it vulnerable to MITM attacks.
# An attacker could intercept traffic, present a fake certificate, and the client would accept it.
def fetch_data_insecurely(url: str):
    print(f"Attempting to fetch data from {url} with verify=False...")
    try:
        response = requests.get(url, verify=False, timeout=5)
        response.raise_for_status() # Raise an exception for HTTP errors
        print(f"Insecure fetch successful from {url}. Status: {response.status_code}")
        print(f"Content snippet: {response.text[:100]}...")
    except requests.exceptions.RequestException as e:
        print(f"Insecure fetch failed for {url}: {e}")

# Example of a legitimate API endpoint
VULNERABLE_API_URL = "https://api.github.com/users/octocat"
fetch_data_insecurely(VULNERABLE_API_URL)

# Even if the URL is HTTPS, verify=False makes it insecure.
# An attacker could proxy this request and serve malicious content.
```

Secure:
```python
import requests
import ssl # To demonstrate default CA paths if needed
import certifi # Provides Mozilla's CA bundle

# By default, requests verifies SSL certificates. It's good practice to explicitly confirm this.
# For custom CAs, specify the path to the CA bundle.
# requests uses certifi by default if available, which is generally recommended.
def fetch_data_securely(url: str, ca_bundle_path: str = None):
    print(f"Attempting to fetch data from {url} with SSL verification enabled...")
    try:
        if ca_bundle_path:
            # Use a specific CA bundle for verification
            response = requests.get(url, verify=ca_bundle_path, timeout=5)
        else:
            # Use default (certifi) CA bundle for verification
            response = requests.get(url, timeout=5) # verify=True is the default
        response.raise_for_status() # Raise an exception for HTTP errors
        print(f"Secure fetch successful from {url}. Status: {response.status_code}")
        print(f"Content snippet: {response.text[:100]}...")
    except requests.exceptions.SSLError as e:
        print(f"Secure fetch failed for {url} due to SSL Error: {e}")
        print("This often means the server's certificate is invalid, expired, or untrusted.")
        print("Ensure the server's certificate is properly configured and trusted by your system/CA bundle.")
    except requests.exceptions.RequestException as e:
        print(f"Secure fetch failed for {url}: {e}")

# Example of a legitimate API endpoint
SECURE_API_URL = "https://api.github.com/users/octocat"
fetch_data_securely(SECURE_API_URL)

# If you need to trust a specific self-signed certificate or a private CA,
# you would provide the path to its .pem file:
# CUSTOM_CA_PATH = "/etc/ssl/certs/my_custom_ca.pem" # Example path
# fetch_data_securely("https://internal-service.example.com", ca_bundle_path=CUSTOM_CA_PATH)

# You can also use certifi.where() to get the path to the default CA bundle
# print(f"Default certifi CA bundle path: {certifi.where()}")
```

Assistant Behavior Guidance:
The AI should issue a high-severity warning whenever `verify=False` is found in `requests` calls or similar HTTP client configurations that disable TLS/SSL certificate verification. The report should clearly state the risk of man-in-the-middle attacks and data interception. It should recommend removing `verify=False` to enable default verification and, if necessary, provide guidance on how to specify a custom CA bundle path for internal or self-signed certificates, emphasizing that disabling verification is almost never an acceptable solution in production environments.

---

# 31. Secure temporary files (tempfile)

Temporary files are often needed by applications for various purposes, such as storing intermediate data, buffering large inputs, or facilitating inter-process communication. However, creating temporary files insecurely can introduce significant vulnerabilities. Common pitfalls include using predictable filenames, which can lead to race conditions (Time-of-Check-to-Time-of-Use, or TOCTOU) where an attacker can guess the filename and create a malicious file before the legitimate application does, or replace the file after it's created but before it's used. This can result in privilege escalation, data leakage, or denial of service. Additionally, insecure permissions on temporary files can allow unauthorized users to read, write, or execute sensitive data. Python's `tempfile` module is specifically designed to address these security concerns by providing functions that create temporary files and directories securely. It generates unique, unpredictable filenames and sets appropriate permissions by default, mitigating race conditions and unauthorized access. Always use `tempfile.mkstemp()` for temporary files and `tempfile.mkdtemp()` for temporary directories, as they return file descriptors and paths that are guaranteed to be unique and created securely. Avoid constructing temporary filenames manually or using `os.mktemp()`, which is deprecated due to its inherent insecurity.

```text
Key Review Checks:
- Are temporary files created using `tempfile.mkstemp()` or `tempfile.TemporaryFile()`?
- Are temporary directories created using `tempfile.mkdtemp()` or `tempfile.TemporaryDirectory()`?
- Is `os.mktemp()` or similar insecure filename generation used?
- Are temporary files/directories cleaned up properly after use (e.g., using `with` statements or explicit deletion)?
- Are sensitive data stored in temporary files adequately protected (e.g., encrypted, restricted permissions)?
```

Vulnerable:
```python
import os
import time

# This approach is vulnerable to race conditions and predictable filenames.
# An attacker could guess the filename and create a malicious file before the application,
# or replace it after creation.
def create_insecure_temp_file(data: str):
    # This is a highly insecure way to create a temporary file.
    # The filename is predictable and there's a race condition between checking existence and creation.
    filename = f"/tmp/app_data_{os.getpid()}_{int(time.time())}.txt"
    print(f"Attempting to create insecure temp file: {filename}")
    try:
        # In a real race condition, an attacker could create this file first
        # or replace it after creation.
        with open(filename, "w") as f:
            f.write(data)
        print(f"Insecure temp file created at {filename}")
        # Simulate reading the file later
        with open(filename, "r") as f:
            read_data = f.read()
            print(f"Read from insecure temp file: {read_data}")
    except Exception as e:
        print(f"Error creating/reading insecure temp file: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Insecure temp file {filename} removed.")

create_insecure_temp_file("Sensitive data that should be secure.")

# Another vulnerable pattern: using os.mktemp (deprecated and insecure)
# def create_another_insecure_temp_file(data: str):
#     filename = os.mktemp() # DEPRECATED and INSECURE
#     print(f"Attempting to create insecure temp file with os.mktemp: {filename}")
#     try:
#         with open(filename, "w") as f:
#             f.write(data)
#         print(f"Insecure temp file created at {filename}")
#     finally:
#         if os.path.exists(filename):
#             os.remove(filename)
#             print(f"Insecure temp file {filename} removed.")
# create_another_insecure_temp_file("More sensitive data.")
```

Secure:
```python
import tempfile
import os

# Using tempfile.mkstemp() for secure temporary file creation.
# It returns a file descriptor and the path, ensuring atomic creation and unique names.
def create_secure_temp_file(data: str):
    print("Attempting to create secure temp file...")
    fd, path = tempfile.mkstemp(suffix=".txt", prefix="secure_app_data_")
    try:
        with os.fdopen(fd, "w") as tmp:
            tmp.write(data)
        print(f"Secure temp file created at {path}")
        # Simulate reading the file later
        with open(path, "r") as tmp_read:
            read_data = tmp_read.read()
            print(f"Read from secure temp file: {read_data}")
    except Exception as e:
        print(f"Error creating/reading secure temp file: {e}")
    finally:
        if os.path.exists(path):
            os.remove(path)
            print(f"Secure temp file {path} removed.")

create_secure_temp_file("Sensitive data that should be secure.")

# Using tempfile.TemporaryFile() for a file-like object that is automatically deleted.
# This is often preferred when you don't need the filename.
def use_secure_temporary_file_object(data: str):
    print("Attempting to use secure temporary file object...")
    try:
        with tempfile.TemporaryFile(mode="w+") as tmp_file:
            tmp_file.write(data)
            tmp_file.seek(0) # Rewind to read
            read_data = tmp_file.read()
            print(f"Read from secure temporary file object: {read_data}")
        print("Secure temporary file object automatically deleted.")
    except Exception as e:
        print(f"Error using secure temporary file object: {e}")

use_secure_temporary_file_object("More sensitive data for temporary processing.")

# Using tempfile.TemporaryDirectory() for secure temporary directory creation.
# It automatically cleans up the directory and its contents.
def use_secure_temporary_directory():
    print("Attempting to use secure temporary directory...")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            print(f"Secure temporary directory created at: {tmpdir}")
            temp_file_path = os.path.join(tmpdir, "my_temp_file.txt")
            with open(temp_file_path, "w") as f:
                f.write("Data inside temp directory.")
            print(f"File created inside temp directory: {temp_file_path}")
        print("Secure temporary directory and its contents automatically deleted.")
    except Exception as e:
        print(f"Error using secure temporary directory: {e}")

use_secure_temporary_directory()
```

Assistant Behavior Guidance:
The AI should flag any manual construction of temporary file paths, especially those incorporating predictable elements like PIDs or timestamps, or the use of `os.mktemp()`. It should explain the race condition and predictable filename vulnerabilities. The report should recommend replacing insecure temporary file creation with `tempfile.mkstemp()`, `tempfile.TemporaryFile()`, or `tempfile.TemporaryDirectory()`, highlighting their benefits in generating unique, secure filenames and handling cleanup.

---

# 32. File permissions and umask

File permissions are a critical aspect of operating system security, controlling who can read, write, or execute files and directories. Incorrectly set permissions can lead to unauthorized access, data leakage, privilege escalation, or denial of service. In Unix-like systems, permissions are typically represented by an octal number (e.g., 0o644 for files, 0o755 for directories) or symbolic notation (e.g., `rwx-r--r--`). The `umask` (user file-creation mode mask) is a system setting that dictates the default permissions for newly created files and directories. It acts as a mask, *removing* permissions from the default full permissions (0o666 for files, 0o777 for directories). For example, a `umask` of 0o022 means that newly created files will have permissions 0o644 (666 - 022) and directories 0o755 (777 - 022). A common security best practice is to ensure that `umask` is set to a restrictive value (e.g., 0o022 or 0o077) to prevent newly created files from being world-writable by default. Applications should also explicitly set appropriate permissions for sensitive files using `os.chmod()` to enforce the principle of least privilege, ensuring that only necessary users or processes have access. Failing to manage file permissions properly can expose sensitive data, configuration files, or logs to unauthorized users or processes.

```text
Key Review Checks:
- Are sensitive files (e.g., configuration, logs, data stores) created with overly permissive permissions?
- Is `os.umask()` explicitly set to a restrictive value at application startup?
- Are `os.chmod()` calls used to tighten permissions on specific files or directories?
- Are files containing secrets (e.g., API keys, database credentials) protected with appropriate permissions (e.g., 0o600)?
- Is the application running with elevated privileges that could lead to insecure file creation?
```

Vulnerable:
```python
import os

# Simulate an insecure umask setting (e.g., 0o000 means full permissions by default)
# In a real scenario, this might be inherited from the environment.
# os.umask(0o000) # For demonstration, do not do this in real code!

def create_insecure_file(filename: str, content: str):
    print(f"Creating file '{filename}' with potentially insecure permissions...")
    try:
        # If umask is 0o000, this file will be created with 0o666 (world-writable)
        # If umask is 0o002, this file will be created with 0o664 (group-writable)
        # If umask is 0o022, this file will be created with 0o644 (only owner writable)
        with open(filename, "w") as f:
            f.write(content)
        # Check actual permissions after creation
        stat_info = os.stat(filename)
        # Permissions are represented by the last 9 bits of st_mode
        permissions = oct(stat_info.st_mode & 0o777)
        print(f"File '{filename}' created with permissions: {permissions}")
        if permissions in ['0o666', '0o664', '0o777', '0o775']:
            print("Vulnerable: File created with overly permissive permissions!")
    except Exception as e:
        print(f"Error creating file: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

# Example: A sensitive configuration file
create_insecure_file("insecure_config.txt", "DB_PASSWORD=mysecretpassword")

# Example: A log file that might contain sensitive information
create_insecure_file("insecure_log.log", "User 'admin' logged in from 192.168.1.100")
```

Secure:
```python
import os
import stat # For symbolic permission constants

# It's good practice to set a restrictive umask at the start of the application
# to ensure newly created files have appropriate default permissions.
# 0o022 (rw-r--r--) for files, (rwxr-xr-x) for directories is a common secure default.
# 0o077 (rw-------) for files, (rwx------) for directories is even more restrictive.
original_umask = os.umask(0o077) # Set umask to be very restrictive (owner only)
print(f"Umask set to 0o077. Original umask was: {oct(original_umask)}")

def create_secure_file(filename: str, content: str, desired_mode: int = 0o600):
    print(f"Creating file '{filename}' with secure permissions...")
    try:
        # Create the file. Its initial permissions will be affected by umask.
        # For example, if umask is 0o077, a file created with default open() will be 0o600.
        with open(filename, "w") as f:
            f.write(content)

        # Explicitly set permissions using os.chmod() to ensure least privilege.
        # This overrides the umask's effect if the umask was less restrictive.
        os.chmod(filename, desired_mode)

        stat_info = os.stat(filename)
        permissions = oct(stat_info.st_mode & 0o777)
        print(f"File '{filename}' created with permissions: {permissions}")
        if permissions == oct(desired_mode):
            print("Secure: File permissions are correctly set.")
        else:
            print(f"Warning: File permissions are {permissions}, expected {oct(desired_mode)}.")
    except Exception as e:
        print(f"Error creating file: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

# Example: A sensitive configuration file, only readable/writable by the owner
create_secure_file("secure_config.txt", "DB_PASSWORD=mysecretpassword", desired_mode=0o600)

# Example: A log file, readable by owner, but not world-readable
create_secure_file("secure_log.log", "User 'admin' logged in from 192.168.1.100", desired_mode=0o640)

# Restore original umask if necessary (e.g., in a library)
# os.umask(original_umask)
```

Assistant Behavior Guidance:
The AI should flag any file creation operations (`open()`, `os.makedirs()`) where sensitive data is involved and explicit permission setting (`os.chmod()`) is absent, or where permissions are set to overly permissive values (e.g., world-writable or group-writable for sensitive files). It should also recommend setting a restrictive `umask` at the application's entry point. The report should explain the risks of insecure file permissions, such as data leakage or unauthorized modification, and provide guidance on using `os.chmod()` with appropriate octal modes (e.g., 0o600 for secrets, 0o644 for general files) and setting `os.umask()` to a secure default like 0o022 or 0o077.

---

# 33. Archive extraction and Zip Slip

Archive extraction, particularly from untrusted sources, presents a significant security risk known as "Zip Slip" or path traversal. This vulnerability occurs when an archive (e.g., a `.zip`, `.tar`, `.rar` file) contains entries with malicious filenames that include path traversal sequences (e.g., `../`, `../../`). When these entries are extracted without proper validation, they can overwrite arbitrary files outside the intended extraction directory. An attacker could craft a malicious archive to overwrite critical system files, configuration files, or even application binaries, leading to denial of service, remote code execution, or privilege escalation. For example, an entry named `../../../../etc/passwd` could overwrite the system's password file. Python's standard library modules like `zipfile` and `tarfile` provide functionalities for archive handling. While these modules themselves are not inherently vulnerable, the *way* they are used can introduce the Zip Slip vulnerability if the extracted filenames are not sanitized and validated against path traversal attempts. It is crucial to always sanitize and validate the full path of each entry before extraction, ensuring that the resolved path remains strictly within the designated target directory.

```text
Key Review Checks:
- Is user-supplied or untrusted archive content being extracted?
- Is the full path of each entry in the archive validated before extraction?
- Are path traversal sequences (e.g., `../`) explicitly checked and rejected or sanitized?
- Is `os.path.abspath()` and `os.path.commonprefix()` or similar logic used to ensure paths stay within the target directory?
- Is `shutil.unpack_archive()` used, and if so, is the source trusted or are additional checks performed?
```

Vulnerable:
```python
import zipfile
import os

# This function is vulnerable to Zip Slip.
# It extracts files without validating their paths, allowing path traversal.
def extract_insecurely(archive_path: str, target_dir: str):
    print(f"Attempting to extract '{archive_path}' to '{target_dir}' insecurely...")
    os.makedirs(target_dir, exist_ok=True)
    try:
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            # This line is the vulnerability: it extracts files directly without path validation.
            zip_ref.extractall(target_dir)
        print(f"Insecure extraction of '{archive_path}' completed.")
    except Exception as e:
        print(f"Error during insecure extraction: {e}")

# Create a dummy malicious zip file for demonstration
# This zip file contains an entry that tries to write outside

---

# 57. Secure HTTP/API clients

When developing Python applications that interact with external services via HTTP or APIs, it is paramount to ensure the security of these communications. This involves more than just sending a request; it encompasses proper handling of SSL/TLS certificates, managing connection timeouts, implementing robust retry mechanisms, and securing sensitive information transmitted in headers or body. Failing to validate SSL/TLS certificates, for instance, opens the door to Man-in-the-Middle (MitM) attacks, where an attacker can intercept, read, and modify traffic between the client and the server without either party knowing. Similarly, neglecting to set appropriate timeouts can lead to denial-of-service vulnerabilities if the client hangs indefinitely waiting for a response from a slow or unresponsive server. Proper error handling and retry logic are also crucial for maintaining application resilience and preventing cascading failures, but these must be implemented carefully to avoid introducing new vulnerabilities like excessive retries that could be exploited for resource exhaustion. Furthermore, sensitive data, such as API keys or authentication tokens, must be transmitted securely, typically over HTTPS, and never exposed in logs or insecure storage. The choice of HTTP client library also matters; `requests` is generally preferred for its user-friendliness and built-in security features compared to lower-level libraries.

```text
Key review checks:
- Is SSL/TLS certificate verification enabled and not bypassed?
- Are appropriate connection and read timeouts configured?
- Is sensitive data (API keys, tokens) transmitted securely (e.g., via Authorization header over HTTPS)?
- Are retry mechanisms implemented with exponential backoff and maximum limits?
- Is the HTTP client library up-to-date and known to be secure?
- Are custom certificate authorities (CAs) handled securely if required?
- Is proxy configuration handled securely, avoiding unauthenticated proxies?
```

Vulnerable:
```python
import requests

# Vulnerable: SSL/TLS verification disabled, susceptible to MitM attacks
def fetch_data_insecure(url):
    try:
        response = requests.get(url, verify=False) # BAD: Disables SSL verification
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Vulnerable: No timeouts, can hang indefinitely
def fetch_data_no_timeout(url):
    try:
        response = requests.get(url) # BAD: No timeout specified
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
```

Secure:
```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Preferred: SSL/TLS verification enabled by default, explicit timeouts, robust retries
def fetch_data_secure(url, api_key):
    session = requests.Session()
    
    # Configure retries with exponential backoff and status code awareness
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter) # Though ideally all traffic should be HTTPS

    headers = {
        "Authorization": f"Bearer {api_key}", # Securely pass API key
        "User-Agent": "SecureAppClient/1.0"
    }
    
    try:
        # Set explicit connection and read timeouts
        # connect timeout: how long to wait for the server to establish a connection
        # read timeout: how long to wait for the server to send a response after connection
        response = session.get(url, headers=headers, timeout=(5, 10)) # GOOD: Explicit timeouts
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.Timeout:
        print("Request timed out.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return None

# Example usage (assuming a secure API key is available)
# API_ENDPOINT = "https://api.example.com/data"
# SECURE_API_KEY = "your_secure_api_key_here"
# data = fetch_data_secure(API_ENDPOINT, SECURE_API_KEY)
# if data:
#     print("Data fetched securely.")
```

Assistant behavior guidance:
When encountering HTTP client code, prioritize checking for disabled SSL/TLS verification (`verify=False`), missing timeouts, and insecure handling of sensitive credentials. If `verify=False` is found, report it as a critical security vulnerability (MitM risk) and explain the implications. For missing timeouts, report it as a high-severity reliability and potential DoS vulnerability. For sensitive data in URLs or insecure headers, report as a high-severity information disclosure. Always recommend using `requests` with explicit timeouts, proper error handling, and secure credential management via `Authorization` headers over HTTPS. Provide examples of robust retry strategies.

---

# 58. Webhook signature verification

Webhook signature verification is a critical security measure for applications that receive webhooks from external services. Without proper verification, an application cannot trust the origin or integrity of incoming webhook payloads, making it vulnerable to spoofing, tampering, and replay attacks. An attacker could forge a webhook payload, pretending to be a legitimate service, and trick the application into performing unauthorized actions or processing malicious data. The standard approach involves the sender computing a cryptographic hash (e.g., HMAC-SHA256) of the payload using a shared secret key and sending this hash in a special HTTP header. The receiver then independently computes the same hash using the same shared secret and compares it to the received signature. If they match, the payload is considered authentic and untampered. Crucially, the comparison must be done using a constant-time string comparison function to prevent timing attacks, where an attacker could deduce parts of the secret key by observing subtle differences in response times. Additionally, webhooks should include a timestamp and the receiver should verify that the timestamp is recent to mitigate replay attacks, where an attacker re-sends an old, legitimate webhook.

```text
Key review checks:
- Is a shared secret used for HMAC signature generation and verification?
- Is the correct hashing algorithm (e.g., HMAC-SHA256) used?
- Is the signature comparison performed using a constant-time function (e.g., `hmac.compare_digest`)?
- Is a timestamp included in the webhook and verified for freshness to prevent replay attacks?
- Is the shared secret stored securely and not hardcoded?
- Is the webhook endpoint protected against unauthenticated access before signature verification?
- Are potential encoding issues (e.g., UTF-8) handled consistently between sender and receiver?
```

Vulnerable:
```python
import hmac
import hashlib
import os
from flask import Flask, request, abort

app = Flask(__name__)

# Vulnerable: Secret hardcoded and comparison is not constant-time
# Vulnerable: No timestamp verification for replay attacks
WEBHOOK_SECRET = "super_secret_key_hardcoded" # BAD: Hardcoded secret

@app.route('/webhook', methods=['POST'])
def webhook_receiver_vulnerable():
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        abort(400, "Signature header missing")

    payload = request.data # Raw body bytes
    
    # BAD: Using regular string comparison, susceptible to timing attacks
    expected_signature = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    if signature != expected_signature: # BAD: Not constant-time comparison
        abort(403, "Invalid signature")

    # Process webhook payload (vulnerable to replay attacks if no timestamp check)
    print("Webhook received and processed (vulnerable).")
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=True)
```

Secure:
```python
import hmac
import hashlib
import os
import time
from flask import Flask, request, abort

app = Flask(__name__)

# Preferred: Secret loaded from environment variable for security
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")
if not WEBHOOK_SECRET:
    raise ValueError("WEBHOOK_SECRET environment variable not set.")

# Define a reasonable tolerance for timestamp freshness (e.g., 5 minutes)
TIMESTAMP_TOLERANCE_SECONDS = 5 * 60

@app.route('/webhook', methods=['POST'])
def webhook_receiver_secure():
    signature_header = request.headers.get('X-Hub-Signature-256')
    timestamp_header = request.headers.get('X-Hub-Timestamp') # Assuming sender provides a timestamp

    if not signature_header or not timestamp_header:
        abort(400, "Signature or Timestamp header missing")

    try:
        # Verify timestamp to prevent replay attacks
        received_timestamp = int(timestamp_header)
        current_time = int(time.time())
        if abs(current_time - received_timestamp) > TIMESTAMP_TOLERANCE_SECONDS:
            abort(403, "Webhook timestamp too old or in the future (possible replay attack)")
    except ValueError:
        abort(400, "Invalid timestamp format")

    payload = request.data # Raw body bytes

    # Extract the signature value (e.g., "sha256=...")
    if not signature_header.startswith("sha256="):
        abort(400, "Invalid signature format")
    
    received_signature = signature_header.split("=", 1)[1]

    # Compute expected signature
    expected_signature_bytes = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest().encode('utf-8') # Encode for comparison

    # Preferred: Use hmac.compare_digest for constant-time comparison
    if not hmac.compare_digest(received_signature.encode('utf-8'), expected_signature_bytes):
        abort(403, "Invalid signature")

    # Webhook is verified, now process the payload
    print("Webhook received and processed securely.")
    # Example: process_webhook_payload(request.json)
    return "OK", 200

if __name__ == '__main__':
    # For production, use a WSGI server like Gunicorn
    # app.run(debug=False, port=5000)
    pass
```

Assistant behavior guidance:
When reviewing webhook endpoints, prioritize checking for the presence and correctness of signature verification. If signature verification is missing or implemented insecurely (e.g., direct string comparison, hardcoded secret, no timestamp check), report it as a critical vulnerability (Spoofing, Tampering, Replay Attacks). Emphasize the use of `hmac.compare_digest` for constant-time comparison and the importance of timestamp verification. Advise loading secrets from environment variables or a secure secret management system. Provide clear examples of how to implement these checks securely.

---

# 59. GraphQL security in Python

GraphQL APIs, while offering flexibility and efficiency, introduce a unique set of security considerations that differ from traditional REST APIs. Without proper safeguards, GraphQL endpoints can be vulnerable to denial-of-service attacks, excessive data exposure, and unauthorized access. One common concern is introspection, which allows clients to query the API's schema. While useful for development tools, introspection can expose sensitive information about the API's structure and underlying data models to attackers. Therefore, introspection should be disabled in production environments or restricted to authenticated and authorized users. Another significant risk is query depth and complexity. Maliciously crafted nested queries can consume excessive server resources, leading to DoS. Implementing query depth limiting and complexity analysis is crucial to prevent such attacks. Authentication and authorization must be rigorously applied at the resolver level, ensuring that users can only access data and perform actions they are permitted to. Batching queries can also be exploited if not properly managed, potentially bypassing rate limits. Furthermore, input validation for arguments and variables is just as important as in REST APIs to prevent injection attacks.

```text
Key review checks:
- Is GraphQL introspection disabled in production environments or restricted to authorized users?
- Are query depth and complexity limits implemented to prevent DoS attacks?
- Is authentication and authorization enforced at the resolver level for all sensitive data and actions?
- Are input arguments and variables properly validated and sanitized?
- Are sensitive fields (e.g., passwords, API keys) excluded from the schema or masked?
- Is batching of queries handled securely, considering rate limits and resource consumption?
- Are error messages generic and do not leak sensitive backend information?
- Is persistent query whitelisting considered for critical production APIs?
```

Vulnerable:
```python
import graphene
from flask import Flask
from flask_graphql import GraphQLView

app = Flask(__name__)

class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    email = graphene.String()
    password_hash = graphene.String() # BAD: Exposing sensitive field

class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.ID(required=True))
    users = graphene.List(User)

    def resolve_user(self, info, id):
        # Vulnerable: No authentication/authorization check
        # Vulnerable: Potential for N+1 query if not optimized
        print(f"Fetching user {id} without auth check.")
        # In a real app, this would fetch from a DB
        if id == "1":
            return User(id="1", username="admin", email="admin@example.com", password_hash="hashed_password_123")
        return None

    def resolve_users(self, info):
        # Vulnerable: No authentication/authorization check, returns all users
        print("Fetching all users without auth check.")
        return [
            User(id="1", username="admin", email="admin@example.com", password_hash="hashed_password_123"),
            User(id="2", username="user", email="user@example.com", password_hash="hashed_password_456")
        ]

schema = graphene.Schema(query=Query)

# Vulnerable: Introspection enabled by default, no query depth/complexity limits
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True) # graphiql=True enables introspection
)

if __name__ == '__main__':
    app.run(debug=True)
```

Secure:
```python
import graphene
from flask import Flask, request, abort
from flask_graphql import GraphQLView
from graphql.validation import ValidationContext, ASTValidationRule
from graphql.error import GraphQLError

app = Flask(__name__)

# --- Security Enhancements ---

# 1. Custom Validation Rule for Query Depth Limiting
class MaxDepthRule(ASTValidationRule):
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.current_depth = 0

    def enter_field(self, node, key, parent, path, ancestors):
        self.current_depth += 1
        if self.current_depth > self.max_depth:
            raise GraphQLError(f"Query exceeds maximum depth of {self.max_depth}", [node])

    def leave_field(self, node, key, parent, path, ancestors):
        self.current_depth -= 1

# 2. Authentication/Authorization Decorator
def login_required(resolver):
    def wrapper(obj, info, **kwargs):
        # In a real app, this would check request.headers for a valid token
        # For demonstration, let's assume a simple header check
        if request.headers.get('Authorization') != 'Bearer valid_token':
            raise GraphQLError("Authentication required", extensions={"code": "UNAUTHENTICATED"})
        return resolver(obj, info, **kwargs)
    return wrapper

def admin_required(resolver):
    def wrapper(obj, info, **kwargs):
        # In a real app, this would check user roles from the token
        if request.headers.get('X-User-Role') != 'admin':
            raise GraphQLError("Admin privileges required", extensions={"code": "UNAUTHORIZED"})
        return resolver(obj, info, **kwargs)
    return wrapper

class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    email = graphene.String()
    # Preferred: Do not expose sensitive fields like password_hash
    # password_hash = graphene.String() 

class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.ID(required=True))
    users = graphene.List(User)

    @login_required
    def resolve_user(self, info, id):
        # Preferred: Input validation for ID (e.g., ensure it's an integer or UUID)
        if not id.isdigit(): # Simple check, use more robust validation for real apps
            raise GraphQLError("Invalid user ID format")
        
        # Preferred: Authorization check for specific user access
        # e.g., if current_user_id != id and not current_user_is_admin: raise GraphQLError(...)
        print(f"Fetching user {id} with auth check.")
        if id == "1":
            return User(id="1", username="admin", email="admin@example.com")
        return None

    @admin_required # Preferred: Restrict access to all users list
    def resolve_users(self, info):
        print("Fetching all users with admin auth check.")
        return [
            User(id="1", username="admin", email="admin@example.com"),
            User(id="2", username="user", email="user@example.com")
        ]

schema = graphene.Schema(query=Query)

# Preferred: Disable GraphiQL (and thus introspection) in production
# Use custom validation rules for query depth/complexity
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=False, # GOOD: Disable GraphiQL/introspection in production
        validation_rules=(MaxDepthRule(max_depth=5),) # GOOD: Apply query depth limit
    )
)

if __name__ == '__main__':
    # For production, ensure debug=False and use a WSGI server
    # app.run(debug=False, port=5000)
    pass
```

Assistant behavior guidance:
When reviewing GraphQL implementations, first check for the presence of `graphiql=True` in production or any other mechanism that enables introspection. If found, report it as a high-severity information disclosure vulnerability. Next, look for missing query depth or complexity limits, reporting this as a high-severity DoS risk. Crucially, verify that authentication and authorization are applied at the resolver level for all sensitive queries and mutations; lack thereof is a critical access control vulnerability. Advise against exposing sensitive fields in the schema and recommend robust input validation. Provide concrete examples of how to implement custom validation rules and authorization decorators.

---

# 60. FastAPI security best practices

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. Its inherent features like Pydantic for data validation and automatic OpenAPI documentation are beneficial for security, but developers must still adhere to best practices to build truly secure applications. Key security considerations include robust authentication and authorization, comprehensive input validation, protection against common web vulnerabilities, and secure configuration. FastAPI integrates seamlessly with OAuth2 for authentication, allowing for secure token-based access. Authorization should be implemented using FastAPI's dependency injection system, ensuring that access checks are performed before sensitive operations. Pydantic models provide excellent input validation, preventing many types of injection and data integrity issues, but custom validation logic might still be necessary for complex scenarios. It's also vital to configure CORS headers correctly to prevent cross-origin attacks, manage sensitive data securely (e.g., API keys, database credentials), and ensure proper error handling that doesn't leak sensitive information. Rate limiting should be considered to prevent abuse and DoS attacks.

```text
Key review checks:
- Is OAuth2/JWT authentication implemented correctly using FastAPI's security dependencies?
- Is authorization enforced using dependency injection at the endpoint level?
- Are Pydantic models used for all incoming request bodies and query parameters, with appropriate validation rules?
- Are custom validation logic and sanitization applied for complex inputs?
- Are CORS headers configured securely, restricting access to known origins?
- Is sensitive configuration data loaded from environment variables or a secure secret manager?
- Are generic error responses provided, avoiding detailed stack traces or internal information?
- Is rate limiting implemented for critical endpoints?
- Are secure HTTP headers (e.g., HSTS, X-Content-Type-Options) configured, possibly via a middleware?
- Is SQL/NoSQL injection prevented through ORMs or parameterized queries?
```

Vulnerable:
```python
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
import os

app = FastAPI()

# Vulnerable: Hardcoded secret key for JWT (if used) or other purposes
# SECRET_KEY = "super_insecure_secret" # BAD: Hardcoded secret

class User(BaseModel):
    username: str
    password: str # BAD: Password sent in plain text, no hashing

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

# Vulnerable: No authentication or authorization
@app.post("/login")
async def login(user: User):
    # BAD: No actual authentication, just accepts any user/pass
    # In a real app, this would check a database
    if user.username == "admin" and user.password == "password":
        return {"message": "Login successful", "token": "insecure_token"} # BAD: Insecure token
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Vulnerable: No authentication or authorization for sensitive operation
@app.post("/items/")
async def create_item(item: Item):
    # BAD: No authorization check, anyone can create items
    print(f"Creating item: {item.name}")
    return item

# Vulnerable: Leaks internal server errors
@app.get("/error_prone")
async def error_prone():
    raise ValueError("This is an internal error!") # BAD: Leaks internal error details if debug is on
```

Secure:
```python
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from typing import Optional
import os
import jwt # PyJWT
from datetime import datetime, timedelta
from passlib.context import CryptContext
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

app = FastAPI()

# --- Security Enhancements ---

# 1. Secure Secret Key from environment variables
SECRET_KEY = os.environ.get("FASTAPI_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("FASTAPI_SECRET_KEY environment variable not set.")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 2. Password Hashing Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 3. OAuth2 Password Bearer for Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 4. User Model with Hashed Password
class UserInDB(BaseModel):
    username: str
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Mock database for demonstration
fake_users_db = {
    "john_doe": UserInDB(username="john_doe", hashed_password=pwd_context.hash("secure_password")),
    "jane_smith": UserInDB(username="jane_smith", hashed_password=pwd_context.hash("another_secure_password")),
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    if username in fake_users_db:
        return fake_users_db[username]
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user

# 5. Secure Item Model with validation
class Item(BaseModel):
    name: str = Field(..., min_length=3, max_length=50) # GOOD: Length validation
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0) # GOOD: Value validation
    tax: Optional[float] = Field(None, ge=0, lt=1) # GOOD: Value validation

# 6. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend.com"], # GOOD: Restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 7. Custom Error Handling Middleware to prevent leaking internal errors
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # Log the exception for internal debugging, but return a generic error to the client
        print(f"An unexpected error occurred: {e}") 
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An internal server error occurred."},
        )

# --- Endpoints ---

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/items/", response_model=Item)
async def create_item(item: Item, current_user: UserInDB = Depends(get_current_user)): # GOOD: Requires authentication
    print(f"User {current_user.username} creating item: {item.name}")
    # In a real app, save item to DB associated with current_user
    return item

@app.get("/users/me/", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user

# Example of an endpoint that might trigger the custom error handler
@app.get("/trigger_error")
async def trigger_error():
    if True: # Simulate a condition that causes an error
        raise ValueError("This is a simulated internal error!")
    return {"message": "This should not be reached"}

if __name__ == '__main__':
    # For production, use a WSGI server like Uvicorn
    # uvicorn main:app --host 0.0.0.0 --port 8000
    pass
```

Assistant behavior guidance:
When reviewing FastAPI applications, prioritize checking for proper authentication and authorization using `Depends` and `OAuth2PasswordBearer`. If authentication is missing or trivially bypassed, report it as a critical access control vulnerability. Verify that Pydantic models are used for all inputs and that fields have appropriate validation rules (e.g., `min_length`, `gt`, `regex`). Flag any hardcoded secrets or sensitive information. Check CORS configuration for overly permissive `allow_origins`. Recommend implementing custom error handling middleware to prevent information leakage and advise on rate limiting for critical endpoints.

---

# 61. Django security middleware and settings

Django is a "batteries-included" web framework, meaning it provides numerous built-in security features and middleware that, when properly configured, significantly reduce the attack surface of web applications. However, these features are only effective if they are correctly enabled and configured. Key security settings include `SECRET_KEY`, which must be a long, random string used for cryptographic signing; `DEBUG`, which should always be `False` in production to prevent information leakage; and `ALLOWED_HOSTS`, which prevents HTTP Host header attacks. Django's middleware stack offers protection against common web vulnerabilities: `CsrfViewMiddleware` protects against Cross-Site Request Forgery (CSRF) attacks, `XFrameOptionsMiddleware` prevents clickjacking, and `SecurityMiddleware` adds various HTTP headers like `X-Content-Type-Options`, `X-XSS-Protection`, and `Strict-Transport-Security` (HSTS) for enhanced browser security. Secure cookie settings (e.g., `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`) are also crucial to prevent cookie theft via XSS. Database connection security, proper user authentication, and authorization are also fundamental.

```text
Key review checks:
- Is `SECRET_KEY` a strong, randomly generated value loaded from environment variables or a secure secret manager?
- Is `DEBUG = False` in production environments?
- Is `ALLOWED_HOSTS` configured correctly to prevent HTTP Host header attacks?
- Are `CsrfViewMiddleware` and `XFrameOptionsMiddleware` enabled in `MIDDLEWARE`?
-

---

