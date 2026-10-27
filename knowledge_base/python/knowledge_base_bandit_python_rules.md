# Bandit Python Security Rules — Detailed RAG Knowledge Base

> **Primary official source:** https://bandit.readthedocs.io/en/latest/
> **Purpose:** Detailed RAG knowledge for the AI Code Review & Security Analysis Agent.

---

# 1. What is Bandit?

Bandit is a static analysis tool designed to find common security issues in Python code. It processes Python code by building an Abstract Syntax Tree (AST) from all files in a specified directory and then runs various plugins against the AST nodes. These plugins are essentially security tests that look for specific patterns or constructs known to be problematic from a security perspective. Bandit is particularly valuable in a Continuous Integration/Continuous Deployment (CI/CD) pipeline, where it can automatically scan code changes and flag potential vulnerabilities before they are deployed to production. This proactive approach helps developers identify and remediate security flaws early in the development lifecycle, significantly reducing the cost and effort associated with fixing them later. It supports a wide range of checks, from hardcoded credentials and insecure deserialization to weak cryptographic algorithms and improper error handling. By integrating Bandit, organizations can enforce security best practices, improve code quality, and reduce their overall attack surface. Its extensible plugin architecture also allows for custom security checks to be added, tailoring its capabilities to specific project needs or compliance requirements.

```text
Key Review Checks/Inputs/Control Flow:
- Static analysis of Python source code.
- Utilizes Abstract Syntax Tree (AST) for code structure analysis.
- Runs a suite of security plugins/tests.
- Designed for integration into CI/CD pipelines.
- Outputs findings in various formats (JSON, XML, text).
- Configurable for specific tests, severities, and confidence levels.
```

Vulnerable:
```python
# Bandit doesn't have a "vulnerable" state itself, but rather analyzes code.
# This example shows a simple Python script that Bandit would analyze.
def insecure_function(password):
    if password == "admin123":
        print("Access granted.")
    else:
        print("Access denied.")

insecure_function("admin123")
```

Secure:
```python
# Bandit doesn't have a "secure" state itself, but rather analyzes code.
# This example shows a simple Python script that Bandit would analyze.
import os

def secure_function(password):
    # Passwords should not be hardcoded or passed directly.
    # This is a placeholder for a more secure authentication mechanism.
    if os.environ.get("APP_PASSWORD") == password:
        print("Access granted.")
    else:
        print("Access denied.")

# secure_function(os.environ.get("USER_INPUT_PASSWORD")) # Example usage
```

Assistant Behavior Guidance:
When encountering a request about Bandit, explain its core function as a Python static analysis security tool. Emphasize its role in identifying common vulnerabilities early in the development cycle and its utility in CI/CD pipelines. Provide context on how it processes code (AST) and its benefits for improving overall application security posture. If specific Bandit rules are mentioned, refer to this knowledge base for detailed explanations of those rules.

---

# 2. Bandit finding structure (JSON schema)

Bandit outputs its findings in a structured format, most commonly JSON, which is highly beneficial for automated processing and integration with other security tools or dashboards. The JSON schema provides a consistent and machine-readable representation of each identified security issue. Key fields within a Bandit finding typically include `filename`, which specifies the file where the issue was found; `line_number` and `col_offset`, pinpointing the exact location; `issue_text`, a human-readable description of the vulnerability; `severity` and `confidence`, indicating the criticality and certainty of the finding; `code`, showing the problematic line of code; `test_id` and `test_name`, identifying the specific Bandit rule triggered; and `more_info`, a URL to further documentation about the rule. This detailed structure allows security teams to programmatically parse results, filter findings based on severity or confidence, track remediation efforts, and generate comprehensive security reports. Understanding this schema is crucial for anyone building tools or scripts that consume Bandit's output, enabling efficient vulnerability management and reporting workflows.

```text
Key Review Checks/Inputs/Control Flow:
- `filename`: Path to the file containing the issue.
- `line_number`, `col_offset`: Precise location of the issue.
- `issue_text`: Description of the vulnerability.
- `severity`: Criticality (LOW, MEDIUM, HIGH).
- `confidence`: Certainty of the finding (LOW, MEDIUM, HIGH).
- `code`: The problematic line of code snippet.
- `test_id`: Unique identifier for the Bandit rule (e.g., B101).
- `test_name`: Human-readable name of the Bandit rule (e.g., assert_used).
- `more_info`: URL to Bandit's documentation for the rule.
- `cwe`: Common Weakness Enumeration ID (if applicable).
```

Vulnerable:
```python
# This is not a code example, but an example of Bandit's JSON output structure.
# A Python script that would trigger a finding:
# def debug_assert(value):
#     assert value, "Value must be true"
# debug_assert(False)
```

Secure:
```python
# This is not a code example, but an example of Bandit's JSON output structure.
# A sample JSON output for a B101 finding:
{
  "errors": [],
  "generated_at": "2023-10-27T10:00:00Z",
  "metrics": {
    "_totals": {
      "LOC": 10,
      "NOSEC": 0,
      "SEVERITY": {
        "HIGH": 0,
        "MEDIUM": 1,
        "LOW": 0
      },
      "CONFIDENCE": {
        "HIGH": 0,
        "MEDIUM": 1,
        "LOW": 0
      }
    }
  },
  "results": [
    {
      "code": "    assert value, \"Value must be true\"",
      "filename": "my_app.py",
      "issue_confidence": "MEDIUM",
      "issue_severity": "MEDIUM",
      "issue_text": "Use of `assert` detected. Asserts can be removed by the Python optimizer.",
      "line_number": 3,
      "col_offset": 5,
      "more_info": "https://bandit.readthedocs.io/en/latest/plugins/b101_assert_used.html",
      "test_id": "B101",
      "test_name": "assert_used"
    }
  ]
}
```

Assistant Behavior Guidance:
When asked about Bandit's output or how to interpret its findings, explain the JSON structure clearly. Detail the purpose of each key field, especially `severity`, `confidence`, `issue_text`, `test_id`, and `more_info`. Emphasize how this structured data facilitates automation, reporting, and integration into vulnerability management systems. Provide an example of a typical JSON finding to illustrate the format.

---

# 3. Severity and confidence model

Bandit employs a two-dimensional model for classifying findings: `severity` and `confidence`. This model helps users prioritize and manage the identified security issues effectively. `Severity` indicates the potential impact of a vulnerability if exploited, typically categorized as `LOW`, `MEDIUM`, or `HIGH`. A `HIGH` severity finding, for instance, might represent a critical remote code execution vulnerability, while a `LOW` severity might be a minor information leak. `Confidence`, on the other hand, reflects how certain Bandit is that a finding is a genuine security issue, also categorized as `LOW`, `MEDIUM`, or `HIGH`. A `HIGH` confidence finding means Bandit is very sure about the issue, often due to a clear, unambiguous pattern match. A `LOW` confidence finding might be a heuristic match that could potentially be a false positive, requiring manual review. Combining these two metrics allows for intelligent prioritization: a `HIGH` severity, `HIGH` confidence finding should be addressed immediately, whereas a `LOW` severity, `LOW` confidence finding might be deferred or ignored after a quick manual check. This model is crucial for reducing alert fatigue and focusing remediation efforts on the most impactful and certain vulnerabilities.

```text
Key Review Checks/Inputs/Control Flow:
- `Severity`: Potential impact of the vulnerability (HIGH, MEDIUM, LOW).
- `Confidence`: Certainty that the finding is a true positive (HIGH, MEDIUM, LOW).
- Prioritization strategy: High Severity + High Confidence = Top Priority.
- False positive reduction: Low Confidence findings may require manual review.
- Configuration options: Users can filter results by minimum severity/confidence.
```

Vulnerable:
```python
# This is not a code example, but a conceptual illustration of how
# severity and confidence are assigned based on code patterns.
# Example: A hardcoded password string (B105) would typically be HIGH severity, HIGH confidence.
password = "mysecretpassword" # This line would trigger B105
```

Secure:
```python
# This is not a code example, but a conceptual illustration of how
# severity and confidence are assigned based on code patterns.
# Example: A try-except-pass (B110) might be MEDIUM severity, MEDIUM confidence.
try:
    # Some operation that might fail
    result = 1 / 0
except Exception:
    pass # This line would trigger B110
```

Assistant Behavior Guidance:
When discussing Bandit findings, always refer to both `severity` and `confidence`. Explain that `severity` indicates potential impact, while `confidence` indicates the likelihood of a true positive. Advise users to prioritize findings with higher severity and confidence first. Suggest that `LOW` confidence findings might warrant manual review to distinguish true positives from false positives, thereby optimizing remediation efforts.

---

# 4. AST analysis capabilities and limitations

Bandit's core strength lies in its use of Abstract Syntax Tree (AST) analysis. When Bandit scans Python code, it doesn't just perform simple text-based pattern matching. Instead, it parses the source code into an AST, which is a tree representation of the program's syntactic structure. This allows Bandit to understand the code's logical flow, variable assignments, function calls, and object relationships, rather than just individual lines of text. For instance, it can differentiate between a string literal that looks like a password and a variable that holds a password, or track if a sensitive value is passed as an argument to an insecure function. This deep understanding enables more accurate detection of vulnerabilities and reduces false positives compared to simpler grep-like tools.

However, AST analysis also has inherent limitations. Bandit operates purely on the static code; it lacks runtime context. It cannot execute the code, understand user input at runtime, or track complex data flows across multiple files or modules, especially when values are dynamically generated or loaded from external sources. This means it might miss vulnerabilities that depend on specific runtime conditions, external configurations, or highly dynamic code generation. For example, if a password is loaded from an environment variable or a database at runtime, Bandit might not be able to trace its usage effectively. Similarly, it struggles with inter-procedural analysis or understanding the full implications of complex object-oriented patterns. These limitations highlight why static analysis tools like Bandit are best used as part of a layered security approach, complemented by dynamic analysis (DAST), interactive analysis (IAST), and manual code reviews.

```text
Key Review Checks/Inputs/Control Flow:
- **Capabilities**:
    - Parses code into a tree structure (AST).
    - Understands code syntax, structure, and basic semantics.
    - Identifies patterns in function calls, variable assignments, imports.
    - More accurate than regex-based scanning.
- **Limitations**:
    - No runtime context or execution.
    - Limited data flow analysis, especially across files/modules.
    - Cannot understand dynamically generated code or external inputs.
    - Prone to false negatives for complex, dynamic vulnerabilities.
    - Does not detect configuration-based vulnerabilities outside code.
```

Vulnerable:
```python
# Bandit can detect a hardcoded password string directly in the AST.
password = "mysecretpassword" # B105
```

Secure:
```python
# Bandit might struggle to track this if 'get_secret' is complex or external.
# However, it would still flag the use of 'os.getenv' as a good practice.
import os

def get_secret(key):
    return os.getenv(key)

password = get_secret("DB_PASSWORD") # Bandit understands os.getenv is used.
```

Assistant Behavior Guidance:
When discussing Bandit's analysis, explain that it uses AST to understand code structure, which is more robust than simple text matching. Clearly articulate its limitations, particularly the lack of runtime context and complex data flow tracking. Advise users that while Bandit is powerful, it should be part of a broader security strategy, not the sole defense, due to these inherent limitations.

---

# 5. B101 — assert_used

The B101 rule flags the use of `assert` statements in Python code. While `assert` statements are excellent for debugging and ensuring internal invariants during development, they are not suitable for security-critical checks in production environments. The primary reason for this is that Python's `assert` statements can be completely removed from the bytecode when the interpreter is run with the `-O` (optimize) or `-OO` (optimize aggressively) flags, or when the `PYTHONOPTIMIZE` environment variable is set. This optimization is intended to improve performance by removing debugging code. However, if a developer uses an `assert` statement to validate user input, check security permissions, or enforce critical preconditions, these checks will silently disappear in an optimized production build, potentially leading to bypassed security controls and exploitable vulnerabilities. Therefore, for any condition that must hold true for the application's security or correct operation, a robust exception-handling mechanism (e.g., `if` statements followed by raising `ValueError`, `TypeError`, or custom exceptions) should be used instead of `assert`.

```text
Key Review Checks/Inputs/Control Flow:
- Presence of `assert` keyword.
- Context of `assert` usage: Is it for debugging or a critical security/logic check?
- Python interpreter flags: `-O` or `-OO` can remove asserts.
- `PYTHONOPTIMIZE` environment variable.
- Replacement: Use `if` statements with explicit exception raising.
```

Vulnerable:
```python
def process_user_input(data):
    # Vulnerable: Assert used for a security-critical input validation
    assert isinstance(data, dict), "Input must be a dictionary"
    assert 'user_id' in data and isinstance(data['user_id'], int), "User ID is required and must be an integer"
    assert data['user_id'] > 0, "User ID must be positive"
    # ... sensitive processing ...
    print(f"Processing data for user {data['user_id']}")

# If run with -O, these checks are removed, allowing invalid input to proceed.
process_user_input({"user_id": -5})
```

Secure:
```python
def process_user_input_secure(data):
    # Preferred: Explicit checks with exceptions for critical validation
    if not isinstance(data, dict):
        raise TypeError("Input must be a dictionary")
    if 'user_id' not in data or not isinstance(data['user_id'], int):
        raise ValueError("User ID is required and must be an integer")
    if data['user_id'] <= 0:
        raise ValueError("User ID must be positive")
    # ... sensitive processing ...
    print(f"Processing data for user {data['user_id']}")

# These checks will always be present, regardless of optimization flags.
try:
    process_user_input_secure({"user_id": -5})
except (TypeError, ValueError) as e:
    print(f"Error: {e}")
```

Assistant Behavior Guidance:
When B101 is detected, explain that `assert` statements are for debugging and can be removed in optimized Python builds. Warn that using them for security-critical validation can lead to bypassed checks. Recommend replacing `assert` with explicit `if` statements that raise appropriate exceptions (e.g., `ValueError`, `TypeError`) to ensure checks are always enforced, regardless of runtime flags.

---

# 6. B102 — exec_used

The B102 rule flags the use of the `exec()` function in Python. The `exec()` function is extremely powerful as it allows executing dynamically generated Python code. While it has legitimate uses in specific scenarios (e.g., metaprogramming, interactive shells), its use with untrusted or unsanitized input is a severe security vulnerability. If an attacker can control any part of the string passed to `exec()`, they can inject arbitrary Python code, leading to remote code execution (RCE). This is one of the most critical types of vulnerabilities, as it grants the attacker full control over the application and the underlying system. Even if the input is seemingly controlled, subtle injection flaws can be difficult to prevent, making `exec()` inherently risky. It's almost always preferable to find alternative, safer ways to achieve dynamic behavior, such as using configuration files, template engines, or carefully designed APIs that do not involve executing arbitrary code. If `exec()` is absolutely necessary, extreme caution and rigorous input sanitization (which is notoriously hard to get right) are required, along with running it in a restricted execution environment if possible.

```text
Key Review Checks/Inputs/Control Flow:
- Presence of `exec()` function call.
- Source of the string passed to `exec()`: Is it user-controlled, external, or hardcoded?
- Input sanitization: Is the input rigorously validated and escaped? (Often insufficient).
- Alternatives: Can the dynamic behavior be achieved with safer constructs?
- Restricted environment: Is `exec()` run with limited globals/locals? (Still risky).
```

Vulnerable:
```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.json.get('code')
    # Vulnerable: Directly executing user-provided code
    exec(code) # B102 triggered here
    return "Code executed", 200

# An attacker could send: {"code": "import os; os.system('rm -rf /')"}
# This allows arbitrary code execution.
```

Secure:
```python
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/process_config', methods=['POST'])
def process_config():
    config_data = request.json.get('config')
    # Preferred: Process configuration data using safe parsing and logic
    # instead of executing arbitrary code.
    try:
        # Example: Safely parse and use a configuration dictionary
        config = json.loads(config_data)
        if config.get('action') == 'log':
            message = config.get('message', 'No message')
            print(f"Log action: {message}")
            return f"Logged: {message}", 200
        else:
            return "Invalid action", 400
    except json.JSONDecodeError:
        return "Invalid JSON config", 400
    except Exception as e:
        return f"Error processing config: {e}", 500

# This approach avoids executing arbitrary code.
```

Assistant Behavior Guidance:
When B102 is found, issue a critical warning about the use of `exec()`. Explain that it allows arbitrary code execution and is a severe security risk, especially with untrusted input. Strongly recommend finding alternative, safer methods for dynamic behavior, such as configuration files, template engines, or carefully designed APIs. If `exec()` is deemed absolutely necessary, advise on extreme caution, rigorous input sanitization, and running in a restricted environment, while still noting the inherent risks.

---

# 7. B103 — set_bad_file_permissions

The B103 rule identifies instances where file permissions are set too broadly, specifically flagging `os.chmod` or `os.fchmod` calls that grant global write access (e.g., `0o777`, `0o666`). Overly permissive file permissions can lead to serious security vulnerabilities. If a file or directory is writable by "other" users (the world), any unprivileged user on the system could potentially modify, delete, or replace its contents. For sensitive files like configuration files, private keys, or application binaries, this could allow an attacker to inject malicious code, alter application behavior, or gain unauthorized access. Even for less sensitive files, it can lead to data integrity issues or denial-of-service by tampering. The principle of least privilege dictates that files and directories should only have the minimum necessary permissions required for their function. Permissions should be carefully chosen, typically restricting write access to the owner or a specific group, and avoiding world-writable permissions unless there's a very specific and well-understood reason (which is rare for security-sensitive files).

```text
Key Review Checks/Inputs/Control Flow:
- Calls to `os.chmod` or `os.fchmod`.
- Permission mode argument: Specifically looking for `0o777`, `0o666`, `0o1777`, etc.
- Context of the file: Is it sensitive data, configuration, or executable?
- Principle of Least Privilege: Are permissions minimal and necessary?
- Alternatives: Use more restrictive modes like `0o644` for files, `0o755` for directories.
```

Vulnerable:
```python
import os

def create_sensitive_file():
    file_path = "/tmp/sensitive_data.txt"
    with open(file_path, "w") as f:
        f.write("This is highly confidential information.")
    # Vulnerable: Setting world-writable permissions
    os.chmod(file_path, 0o777) # B103 triggered here
    print(f"File created with insecure permissions: {file_path}")

create_sensitive_file()
```

Secure:
```python
import os

def create_secure_file():
    file_path = "/tmp/secure_data.txt"
    with open(file_path, "w") as f:
        f.write("This is highly confidential information.")
    # Preferred: Setting restrictive permissions (owner read/write, group/others read-only)
    os.chmod(file_path, 0o644) # Secure permissions
    print(f"File created with secure permissions: {file_path}")

create_secure_file()
```

Assistant Behavior Guidance:
When B103 is detected, explain that setting overly permissive file permissions (e.g., `0o777`, `0o666`) creates a security risk by allowing unauthorized users to modify or delete sensitive files. Emphasize the principle of least privilege. Recommend using more restrictive permissions, such as `0o644` for files (owner read/write, others read-only) or `0o755` for directories (owner read/write/execute, others read/execute), to protect data integrity and confidentiality.

---

# 8. B104 — hardcoded_bind_all_interfaces

The B104 rule flags instances where a network service is configured to listen on all available network interfaces, typically by binding to the IP address `0.0.0.0` or `::` (for IPv6). While binding to all interfaces can be convenient for development or in environments where the service needs to be accessible from multiple network segments, it poses a security risk in production if not explicitly intended. By default, services should only bind to the specific interfaces they need to serve. Binding to `0.0.0.0` means the service will accept connections from any network interface, including external, public-facing ones. If the service is not properly secured (e.g., lacks authentication, authorization, or encryption), or if it contains vulnerabilities, exposing it to the entire network can make it easily discoverable and exploitable by attackers. This is particularly dangerous for administrative interfaces, debugging ports, or services that are only meant for internal communication. The best practice is to bind to `127.0.0.1` (localhost) if the service is only for local access, or to a specific internal IP address if it's meant for internal network access only.

```text
Key Review Checks/Inputs/Control Flow:
- Network binding configuration: `socket.bind()`, `app.run(host=...)`, `server.listen()`.
- IP address used for binding: Specifically `0.0.0.0` or `::`.
- Service type: Is it an internal service, administrative interface, or public-facing?
- Network exposure: Is the host accessible from external networks?
- Principle of Least Exposure: Bind only to necessary interfaces.
```

Vulnerable:
```python
import socket
from flask import Flask

# Vulnerable: Binding to all interfaces (0.0.0.0)
# This exposes the service to all networks the host is connected to.
HOST = '0.0.0.0' # B104 triggered here
PORT = 8080

# Example 1: Raw socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print(f"Listening on {HOST}:{PORT} (Vulnerable)")
s.close()

# Example 2: Flask app
app = Flask(__name__)
@app.route('/')
def hello():
    return "Hello, World!"

# app.run(host=HOST, port=PORT) # This would also trigger B104 if uncommented.
```

Secure:
```python
import socket
from flask import Flask

# Preferred: Binding to localhost (127.0.0.1) for local access only
# or a specific internal IP address if intended for internal network.
HOST_LOCAL = '127.0.0.1'
PORT_SECURE = 8081

# Example 1: Raw socket
s_secure = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_secure.bind((HOST_LOCAL, PORT_SECURE))
s_secure.listen(1)
print(f"Listening on {HOST_LOCAL}:{PORT_SECURE} (Secure)")
s_secure.close()

# Example 2: Flask app
app_secure = Flask(__name__)
@app_secure.route('/')
def hello_secure():
    return "Hello, Secure World!"

# app_secure.run(host=HOST_LOCAL, port=PORT_SECURE) # Secure binding
```

Assistant Behavior Guidance:
When B104 is detected, explain that binding to `0.0.0.0` or `::` exposes a service to all network interfaces, which can be a security risk if the service is not intended for public access or is vulnerable. Recommend binding to `127.0.0.1` (localhost) for local-only services or a specific internal IP address for services meant for internal networks, adhering to the principle of least exposure.

---

# 9. B105 — hardcoded_password_string

The B105 rule flags instances where a password or other sensitive credential is hardcoded directly as a string literal within the source code. This is a critical security vulnerability because hardcoded credentials are easily discoverable by anyone with access to the codebase, including developers, auditors, or attackers who manage to compromise the source repository. Once exposed, these credentials can be used to gain unauthorized access to systems, databases, APIs, or other sensitive resources. Furthermore, changing a hardcoded password requires modifying and redeploying the code, which is cumbersome and prone to errors. Best practices dictate that sensitive credentials should never be stored directly in source code. Instead, they should be managed securely using environment variables, dedicated secret management services (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault), or secure configuration files that are properly protected and excluded from version control. This approach ensures that credentials can be rotated easily, are not exposed in code, and are managed separately from the application logic.

```text
Key Review Checks/Inputs/Control Flow:
- String literals assigned to variables named "password", "secret", "key", "token", etc.
- String literals used directly in authentication functions or API calls.
- Presence of common password patterns or entropy in string literals.
- Alternatives: Environment variables, secret management services, secure config files.
- Exclusion from version control: `.gitignore` for config files.
```

Vulnerable:
```python
# Vulnerable: Hardcoded password as a string literal
DB_PASSWORD = "my_super_secret_db_password123!" # B105 triggered here
API_KEY = "sk_live_abcdef1234567890" # B105 triggered here

def connect_to_database():
    print(f"Connecting to DB with password: {DB_PASSWORD}")
    # ... database connection logic ...

connect_to_database()
```

Secure:
```python
import os

# Preferred: Retrieving sensitive credentials from environment variables
# or a dedicated secret management service.
DB_PASSWORD = os.getenv("DB_PASSWORD")
API_KEY = os.getenv("API_KEY")

def connect_to_database_secure():
    if DB_PASSWORD:
        print("Connecting to DB using environment variable password.")
        # ... secure database connection logic ...
    else:
        print("DB_PASSWORD environment variable not set. Cannot connect.")

connect_to_database_secure()
```

Assistant Behavior Guidance:
When B105 is detected, issue a critical security alert. Explain that hardcoding passwords or sensitive keys directly in the source code is a severe vulnerability, making them easily discoverable. Strongly recommend moving all sensitive credentials to environment variables, a dedicated secret management system, or securely managed configuration files that are excluded from version control. Emphasize the importance of credential rotation and the principle of least privilege.

---

# 10. B106 — hardcoded_password_funcarg

The B106 rule flags instances where a hardcoded password or sensitive credential is passed directly as a string literal argument to a function call. This is similar to B105 but specifically targets function arguments, which often represent interactions with external systems or security-sensitive operations. Passing a hardcoded string directly as an argument, especially to functions related to authentication, database connections, API calls, or cryptographic operations, exposes the credential in the source code. This makes it vulnerable to discovery by anyone with access to the codebase, leading to unauthorized access or system compromise. Even if the function itself is secure, the act of hardcoding the credential in the call site undermines the overall security posture. The same remediation strategies as B105 apply: sensitive credentials should be retrieved from secure sources like environment variables, secret management services, or encrypted configuration files at runtime, rather than being embedded directly into the code. This ensures that credentials remain out of source control and can be managed independently of the application's deployment.

```text
Key Review Checks/Inputs/Control Flow:
- Function calls where arguments are string literals.
- Argument names or function names indicating sensitive operations (e.g., `password=`, `key=`, `authenticate()`, `connect()`).
- Direct string literal values for sensitive parameters.
- Alternatives: Load

---

# 21. B304 — insecure ciphers

This rule identifies the use of insecure or deprecated cryptographic ciphers within Python applications. Cryptographic ciphers are fundamental components for ensuring the confidentiality and integrity of data, but their security strength can degrade over time due to advances in cryptanalysis or computational power. Using ciphers that are known to be weak, have published vulnerabilities, or are considered deprecated by cryptographic standards bodies (like NIST) can expose sensitive data to decryption by attackers. For instance, ciphers like DES (Data Encryption Standard) or RC4 are no longer considered secure for most applications due to their small key sizes or known weaknesses, making them susceptible to brute-force attacks or specific cryptanalytic attacks. The impact of using an insecure cipher can range from unauthorized disclosure of confidential information to the complete compromise of data integrity, leading to severe financial, reputational, and legal consequences for an organization. It is crucial to employ modern, strong, and well-vetted ciphers that are resistant to current attack methodologies and adhere to industry best practices for data protection. Developers should regularly review and update the cryptographic primitives used in their applications to stay ahead of evolving threats.

```text
Key Review Checks:
- Identification of cryptographic library usage (e.g., `cryptography`, `PyCryptodome`).
- Specific cipher algorithms being instantiated or configured.
- Look for `DES`, `3DES` (Triple DES), `RC4`, `Blowfish`, `IDEA`, `MD5` (when used for encryption/key derivation, not just hashing), `SHA1` (when used for encryption/key derivation).
- Check for hardcoded cipher suites in TLS/SSL contexts that include weak ciphers.
- Review `Cipher.algorithms` and `Cipher.modes` for deprecated options.
```

Vulnerable:
```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

key = os.urandom(8) # DES uses 8-byte key (56-bit effective)
iv = os.urandom(8)

# Using DES, which is a known insecure cipher
cipher = Cipher(algorithms.DES(key), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
plaintext = b"This is a secret message."
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

print(f"DES Ciphertext: {ciphertext.hex()}")
```

Secure:
```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Use AES-256, a modern and strong cipher
key = os.urandom(32) # AES-256 uses a 32-byte key
iv = os.urandom(16) # AES uses a 16-byte IV for CBC mode

cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
plaintext = b"This is a secret message that needs strong protection."
# Pad the plaintext to be a multiple of the block size (16 bytes for AES)
from cryptography.hazmat.primitives import padding
padder = padding.PKCS7(algorithms.AES.block_size).padder()
padded_plaintext = padder.update(plaintext) + padder.finalize()

ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

print(f"AES-256 Ciphertext: {ciphertext.hex()}")
```

Assistant behavior guidance:
The AI should report this as a "High" severity issue, indicating that the application is using an insecure or deprecated cryptographic cipher. The report should clearly state the specific cipher identified (e.g., DES, RC4) and explain why it is considered insecure, referencing known vulnerabilities or cryptographic weaknesses. It should advise the developer to migrate to modern, strong, and industry-recommended ciphers such as AES-256 in an authenticated mode like GCM or CCM, or AES-128 if performance is critical and key management is robust. The AI should also suggest reviewing the entire cryptographic implementation to ensure all components adhere to current security standards and to consider using high-level cryptographic libraries that abstract away complex primitive choices, reducing the chance of misconfiguration.

---

# 22. B305 — insecure cipher modes

This rule flags the use of insecure or inappropriate cipher modes of operation. While the underlying cipher algorithm (e.g., AES) might be strong, the way it is applied to encrypt data in blocks (its mode of operation) can introduce severe vulnerabilities if chosen or implemented incorrectly. A classic example of an insecure mode is Electronic Codebook (ECB). In ECB mode, each block of plaintext is encrypted independently with the same key. This means identical plaintext blocks will always produce identical ciphertext blocks, revealing patterns in the original data. For instance, an image encrypted with ECB mode will still show the outline of the original image, demonstrating its weakness in hiding data patterns. This lack of semantic security makes ECB unsuitable for most applications, especially when encrypting data with repetitive patterns or when confidentiality of patterns is critical. Other modes, like Cipher Block Chaining (CBC), are generally more secure than ECB but still require a unique and unpredictable Initialization Vector (IV) for each encryption operation to prevent identical plaintext prefixes from producing identical ciphertext prefixes. Without proper IV management, CBC can also become vulnerable. Authenticated encryption modes like GCM (Galois/Counter Mode) or CCM (Counter with CBC-MAC) are preferred as they provide both confidentiality and integrity, protecting against both passive eavesdropping and active tampering.

```text
Key Review Checks:
- Identification of cryptographic library usage (e.g., `cryptography`, `PyCryptodome`).
- Specific cipher modes being instantiated or configured.
- Look for `modes.ECB`.
- Check for `modes.CBC` without proper, randomly generated, and unique IVs for each encryption.
- Review `Cipher.modes` for deprecated or known weak modes.
```

Vulnerable:
```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

key = os.urandom(32) # AES-256 key
# Using ECB mode, which is insecure because it encrypts identical blocks identically
cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
encryptor = cipher.encryptor()

# Example plaintext with repetitive blocks
plaintext = b"secretsecretsecretsecretsecretsecretsecretsecret"
# Pad the plaintext to be a multiple of the block size (16 bytes for AES)
from cryptography.hazmat.primitives import padding
padder = padding.PKCS7(algorithms.AES.block_size).padder()
padded_plaintext = padder.update(plaintext) + padder.finalize()

ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

print(f"ECB Ciphertext (shows patterns): {ciphertext.hex()}")
```

Secure:
```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

key = os.urandom(32) # AES-256 key
# Using GCM mode, which provides authenticated encryption (confidentiality and integrity)
# GCM requires a unique nonce (IV) for each encryption operation
nonce = os.urandom(16) # GCM nonce is typically 12 or 16 bytes

cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
encryptor = cipher.encryptor()

plaintext = b"This is a secret message that needs strong protection and integrity."
# No padding needed for GCM as it's a stream cipher mode

ciphertext = encryptor.update(plaintext) + encryptor.finalize()
tag = encryptor.tag # GCM produces an authentication tag

print(f"GCM Ciphertext (secure, no patterns): {ciphertext.hex()}")
print(f"GCM Tag: {tag.hex()}")
```

Assistant behavior guidance:
The AI should flag this as a "High" severity issue, specifically identifying the use of an insecure cipher mode, such as ECB. The report must explain *why* the identified mode is insecure, highlighting its vulnerability to pattern leakage and lack of semantic security. It should strongly recommend migrating to authenticated encryption modes like AES-GCM or AES-CCM, which provide both confidentiality and integrity protection. For modes like CBC, the AI should emphasize the critical requirement for a unique, randomly generated, and non-predictable Initialization Vector (IV) for each encryption operation, and warn against reusing IVs or using static IVs. The guidance should stress that even with a strong underlying cipher, an insecure mode can completely undermine the security of encrypted data.

---

# 23. B306 — mktemp_q

This rule identifies the use of `os.mktemp()` for creating temporary files. The `os.mktemp()` function is considered insecure and has been deprecated in Python 3.x because it is susceptible to race conditions. A race condition occurs when multiple processes or threads attempt to access or modify the same resource (in this case, a file name) in an uncontrolled sequence. Specifically, `os.mktemp()` generates a unique temporary filename but does not create the file itself. There is a time window between when `os.mktemp()` returns a filename and when the application actually creates the file using that name. During this window, a malicious actor could create a file with the same name, potentially leading to various attacks. These attacks include:
1.  **Symlink attacks:** An attacker could create a symbolic link pointing to an arbitrary system file (e.g., `/etc/passwd`). When the legitimate application later attempts to write to the temporary file, it would inadvertently write to the system file, potentially corrupting it or elevating privileges.
2.  **Information leakage:** An attacker could create the file with sensitive content, and if the legitimate application later reads from it, it might process attacker-controlled data.
3.  **Denial of Service:** An attacker could create the file and set restrictive permissions, preventing the legitimate application from accessing it.

Due to these severe security implications, `os.mktemp()` should never be used. The recommended secure alternative is `tempfile.mkstemp()` or `tempfile.TemporaryFile()`, which create and open the temporary file atomically, preventing race conditions.

```text
Key Review Checks:
- Direct calls to `os.mktemp()`.
- Usage of `os.mktemp()` in conjunction with file creation operations.
- Any custom temporary file generation logic that mimics `os.mktemp()`'s behavior (generate name, then create).
```

Vulnerable:
```python
import os
import time

def process_data_in_temp_file(data):
    # Vulnerable: os.mktemp() is susceptible to race conditions
    temp_filename = os.mktemp(suffix=".tmp", prefix="data_")
    print(f"Generated temp filename: {temp_filename}")

    # In a real-world scenario, a malicious actor could create this file
    # or a symlink to a sensitive file in the brief moment between
    # os.mktemp() returning and the file being opened here.
    try:
        with open(temp_filename, "w") as f:
            f.write(data)
        print(f"Data written to {temp_filename}")
        # Simulate some processing
        time.sleep(0.1)
        with open(temp_filename, "r") as f:
            read_data = f.read()
        print(f"Data read from {temp_filename}: {read_data}")
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            print(f"Cleaned up {temp_filename}")

process_data_in_temp_file("Some sensitive data to process.")
```

Secure:
```python
import tempfile
import os

def process_data_in_temp_file_secure(data):
    # Secure: tempfile.mkstemp() creates and opens the file atomically
    # It returns a file descriptor and the path.
    fd, temp_filepath = tempfile.mkstemp(suffix=".tmp", prefix="secure_data_")
    print(f"Generated secure temp filepath: {temp_filepath}")

    try:
        # Use the file descriptor for writing
        with os.fdopen(fd, "w") as f:
            f.write(data)
        print(f"Data written to {temp_filepath}")

        # Re-open the file by path for reading if necessary, or use the fd directly
        with open(temp_filepath, "r") as f:
            read_data = f.read()
        print(f"Data read from {temp_filepath}: {read_data}")
    finally:
        # Ensure the temporary file is removed
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
            print(f"Cleaned up {temp_filepath}")

process_data_in_temp_file_secure("Some sensitive data to process securely.")

# Alternatively, for a file-like object that is automatically deleted on close:
def process_data_in_temp_file_object(data):
    with tempfile.TemporaryFile(mode="w+") as tf:
        tf.write(data)
        tf.seek(0) # Rewind to read
        read_data = tf.read()
        print(f"Data processed using TemporaryFile object: {read_data}")

process_data_in_temp_file_object("Another piece of secure data.")
```

Assistant behavior guidance:
The AI should report this as a "High" severity issue, clearly stating that `os.mktemp()` is being used, which is insecure due to race conditions. The report should detail the potential attack vectors, such as symlink attacks, information leakage, and denial of service, emphasizing the critical risk of arbitrary file overwrites or privilege escalation. It must strongly recommend replacing `os.mktemp()` with `tempfile.mkstemp()` or `tempfile.TemporaryFile()`, explaining that these functions create and open the temporary file atomically, thereby eliminating the race condition. The AI should also advise reviewing any custom temporary file creation logic to ensure it doesn't suffer from similar race condition vulnerabilities.

---

# 24. B307 — eval

This rule identifies the use of the `eval()` function, which is a powerful built-in Python function that parses and executes a Python expression passed as a string argument. While `eval()` can be useful for dynamic code execution in controlled environments, it poses a severe security risk when used with untrusted or user-supplied input. If an attacker can control the string passed to `eval()`, they can execute arbitrary Python code within the context of the application. This can lead to a wide range of devastating consequences, including:
1.  **Remote Code Execution (RCE):** The attacker can execute system commands, access files, or manipulate application logic.
2.  **Information Disclosure:** The attacker can read sensitive files (e.g., configuration files, private keys) from the server.
3.  **Data Tampering:** The attacker can modify or delete data.
4.  **Denial of Service:** The attacker can introduce infinite loops or resource-intensive operations to crash the application.

Even when `eval()` is used with `globals` and `locals` dictionaries to restrict its environment, it is notoriously difficult to completely sandbox it securely. Many bypass techniques exist, making it an extremely dangerous function for processing external input. Therefore, `eval()` should almost always be avoided, especially in web applications or any system that processes external data. Safer alternatives usually involve parsing input into a data structure (e.g., JSON, YAML) or using a limited expression parser if dynamic evaluation is truly necessary.

```text
Key Review Checks:
- Direct calls to `eval()`.
- `eval()` used with user-controlled input, query parameters, or data from external sources.
- `eval()` used in conjunction with `input()` or `raw_input()`.
- `eval()` used in template engines or configuration parsing where input might be untrusted.
```

Vulnerable:
```python
import sys

def calculate_expression_vulnerable(expression_string):
    """
    Vulnerable function that uses eval() with potentially untrusted input.
    An attacker could inject malicious Python code here.
    """
    print(f"Evaluating: {expression_string}")
    try:
        # If expression_string comes from user input, this is a critical vulnerability.
        result = eval(expression_string)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error during evaluation: {e}")

# Example of legitimate use (but still risky if input is not strictly controlled)
calculate_expression_vulnerable("2 + 3 * 4")

# Example of a malicious payload if an attacker controls the input
# This could delete files, execute system commands, or steal data.
# For demonstration, this will print a message, but could be os.system('rm -rf /')
malicious_payload = "__import__('os').system('echo ATTACKER EXECUTED COMMAND: ls -la /tmp')"
print("\n--- Simulating malicious input ---")
calculate_expression_vulnerable(malicious_payload)

# Another example: reading sensitive files
malicious_read_file = "__import__('builtins').open('/etc/passwd').read()"
print("\n--- Simulating malicious file read ---")
# calculate_expression_vulnerable(malicious_read_file) # Uncomment to see the effect
```

Secure:
```python
import ast
import operator

# A safer way to evaluate simple arithmetic expressions
# This approach uses ast.literal_eval for safe parsing and a whitelist of operations.

class SafeCalculator:
    def __init__(self):
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.USub: operator.neg,
            ast.Pow: operator.pow, # Be careful with power, can be resource intensive
        }

    def evaluate(self, node):
        if isinstance(node, ast.Num): # <number>
            return node.n
        elif isinstance(node, ast.BinOp): # <left> <op> <right>
            return self.operators[type(node.op)](self.evaluate(node.left), self.evaluate(node.right))
        elif isinstance(node, ast.UnaryOp): # <op> <operand>
            return self.operators[type(node.op)](self.evaluate(node.operand))
        else:
            raise TypeError(node)

    def calculate_expression_secure(self, expression_string):
        """
        Secure function that evaluates arithmetic expressions using ast.literal_eval
        and a custom AST walker, preventing arbitrary code execution.
        """
        print(f"Safely evaluating: {expression_string}")
        try:
            # ast.literal_eval safely evaluates literals (strings, numbers, lists, dicts, tuples, booleans, None)
            # It does NOT execute arbitrary code.
            # For more complex arithmetic, we can parse the AST and walk it.
            tree = ast.parse(expression_string, mode='eval')
            result = self.evaluate(tree.body)
            print(f"Result: {result}")
        except (ValueError, TypeError, SyntaxError) as e:
            print(f"Error during safe evaluation: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

calculator = SafeCalculator()
calculator.calculate_expression_secure("2 + 3 * 4")
calculator.calculate_expression_secure("10 / 2 - 1")
calculator.calculate_expression_secure("pow(2, 8)") # This will fail because pow is not in our whitelist
calculator.calculate_expression_secure("__import__('os').system('echo This should not run')") # This will fail
```

Assistant behavior guidance:
The AI should report this as a "Critical" severity issue, emphasizing that `eval()` with untrusted input is a direct path to Remote Code Execution (RCE). The report should clearly state that `eval()` allows arbitrary Python code execution and detail the severe consequences, including data theft, system compromise, and denial of service. It must strongly recommend removing all instances of `eval()` that process external or user-controlled input. The AI should suggest alternative approaches such as:
1.  Using `ast.literal_eval()` for safely evaluating Python literals (strings, numbers, lists, dicts, tuples, booleans, None).
2.  Implementing a custom parser or a domain-specific language (DSL) for specific evaluation needs.
3.  Serializing data using safer formats like JSON or YAML and then deserializing them.
4.  For complex mathematical expressions, consider using libraries like `numexpr` or building a restricted AST walker.
The AI should also warn against attempts to "sandbox" `eval()` using `globals` and `locals` arguments, as these are often bypassable and do not provide robust security.

---

# 25. B308 — mark_safe

This rule specifically targets the use of `django.utils.safestring.mark_safe()` in Django applications. While `mark_safe()` is a legitimate and necessary function in Django's templating system, its incorrect usage can introduce severe Cross-Site Scripting (XSS) vulnerabilities. Django's template engine, by default, escapes all output to prevent XSS attacks. `mark_safe()` explicitly tells Django that a given string is "safe" and should not be escaped. This is intended for situations where the developer is absolutely certain that the string contains valid, harmless HTML that needs to be rendered directly (e.g., pre-rendered HTML snippets from a trusted source, or HTML generated by a trusted rich-text editor).

The vulnerability arises when `mark_safe()` is applied to strings that contain or could potentially contain user-supplied input without proper sanitization. If an attacker can inject malicious HTML or JavaScript into a string that is then marked as safe, their code will be executed in the user's browser. This can lead to:
1.  **Session Hijacking:** Stealing user cookies and session tokens.
2.  **Defacement:** Modifying the appearance of the webpage.
3.  **Redirection:** Redirecting users to malicious sites.
4.  **Phishing:** Displaying fake login forms to steal credentials.
5.  **Malware Distribution:** Forcing users to download malicious files.

Therefore, `mark_safe()` should only be used when the content is guaranteed to be safe, either because it's hardcoded, comes from a fully trusted source, or has undergone rigorous, context-aware sanitization *before* being marked safe. Never apply `mark_safe()` directly to raw user input.

```text
Key Review Checks:
- Calls to `django.utils.safestring.mark_safe()`.
- `mark_safe()` applied to variables that originate from user input (e.g., request parameters, form fields, database entries populated by users).
- `mark_safe()` used on strings concatenated with user input.
- Lack of explicit sanitization (e.g., using a library like `Bleach`) before `mark_safe()`.
```

Vulnerable:
```python
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def vulnerable_view(request: HttpRequest):
    user_input = request.GET.get('comment', '<script>alert("XSS!");</script>')
    # Vulnerable: User input is directly marked as safe without sanitization.
    # An attacker can inject arbitrary HTML/JavaScript.
    safe_comment = mark_safe(f"<div>User comment: {user_input}</div>")

    context = {
        'display_content': safe_comment
    }
    return render(request, 'vulnerable_template.html', context)

# vulnerable_template.html (simplified)
# <html><body>{{ display_content }}</body></html>
```

Secure:
```python
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import bleach # A robust HTML sanitization library

def secure_view(request: HttpRequest):
    user_input = request.GET.get('comment', '<script>alert("XSS!");</script>')

    # Secure: Sanitize user input before marking it safe.
    # bleach.clean() removes unwanted tags and attributes.
    # Define allowed tags and attributes carefully.
    allowed_tags = ['p', 'b', 'i', 'a', 'div', 'span']
    allowed_attrs = {'a': ['href', 'title']}
    sanitized_input = bleach.clean(user_input, tags=allowed_tags, attributes=allowed_attrs, strip=True)

    # Now, the sanitized input can be safely embedded into HTML and marked safe.
    # Alternatively, if no HTML is expected, simply don't use mark_safe and let Django escape it.
    safe_comment = mark_safe(f"<div>User comment: {sanitized_input}</div>")

    context = {
        'display_content': safe_comment
    }
    return render(request, 'secure_template.html', context)

# secure_template.html (simplified)
# <html><body>{{ display_content }}</body></html>

def another_secure_view(request: HttpRequest):
    user_input = request.GET.get('name', '<b>John Doe</b>')
    # Most secure: Let Django's templating engine handle escaping by default.
    # Only use mark_safe if you are absolutely sure the content is trusted HTML.
    # If user_input is just text, no need for mark_safe.
    context = {
        'display_name': user_input # Django will automatically escape this
    }
    return render(request, 'another_secure_template.html', context)

# another_secure_template.html (simplified)
# <html><body>Hello, {{ display_name }}!</body></html>
```

Assistant behavior guidance:
The AI should report this as a "High" severity issue, specifically identifying the use of `mark_safe()` on potentially untrusted input. The report should clearly explain that this practice leads to Cross-Site Scripting (XSS) vulnerabilities, detailing the potential impact (session hijacking, data theft, defacement). It must strongly advise against using `mark_safe()` directly on any user-supplied or external data without prior, robust, context-aware sanitization. The AI should recommend using a dedicated HTML sanitization library like `Bleach` to filter user input before marking it safe. Furthermore, it should emphasize that the default behavior of Django's template engine (auto-escaping) is the preferred and safest approach for displaying user-generated content, and `mark_safe()` should only be used as an exception for truly trusted HTML.

---

# 26. B310 — urllib_urlopen

This rule flags the use of `urllib.request.urlopen()` (or `urllib.urlopen()` in Python 2) without proper validation, which can lead to several security issues, most notably Server-Side Request Forgery (SSRF) and insecure handling of SSL/TLS certificates.

**Server-Side Request Forgery (SSRF):** If the URL passed to `urlopen()` is controlled or influenced by user input, an attacker can trick the server into making requests to internal network resources (e.g., internal APIs, databases, cloud metadata services like AWS EC2 metadata service `http://169.254.169.254/latest/meta-data/`) or to external malicious sites. This can lead to:
1.  **Information Disclosure:** Accessing sensitive internal data.
2.  **Port Scanning:** Mapping internal network topology.
3.  **Internal Service Interaction:** Triggering actions on internal services.
4.  **Bypassing Firewalls:** Using the server as a proxy to attack other systems.

**Insecure SSL/TLS Handling:** By default, `urllib.request.urlopen()` performs SSL/TLS certificate verification. However, developers sometimes disable this verification (e.g., by passing `context=ssl._create_unverified_context()`) to bypass certificate errors, especially in development or with self-signed certificates. Disabling verification makes the connection vulnerable to Man-in-the-Middle (MitM) attacks, where an attacker can intercept and tamper with encrypted traffic without being detected. This compromises the confidentiality and integrity of the communication.

While `urllib.request.urlopen()` itself isn't inherently insecure, its usage patterns often introduce vulnerabilities when not handled carefully. It's generally recommended to use a more robust HTTP client library like `requests`, which offers better security defaults, easier certificate management, and more control over request parameters.

```text
Key Review Checks:
- Calls to `urllib.request.urlopen()` or `urllib.urlopen()`.
- URL parameter to `urlopen()` originates from user input, query strings, or external configuration.
- Lack of URL validation (e.g., whitelisting allowed domains, schemes, or IP ranges).
- Usage of `ssl._create_unverified_context()` when making HTTPS requests with `urlopen()`.
```

Vulnerable:
```python
import urllib.request
import ssl

def fetch_url_vulnerable(url):
    """
    Vulnerable function:
    1. URL can be user-controlled, leading to SSRF.
    2. SSL verification is explicitly disabled, leading to MitM risk.
    """
    print(f"Attempting to fetch (vulnerable): {url}")
    try:
        # Vulnerability 1: SSRF if 'url' is user-controlled.
        # Vulnerability 2: Disabling SSL verification exposes to MitM attacks.
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=context, timeout=5) as response:
            print(f"Status: {response.status}")
            print(f"Headers: {response.headers}")
            content = response.read().decode('utf-8')
            print(f"Content snippet: {content[:200]}...")
    except urllib.error.URLError as e:
        print(f"URLError: {e.reason}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example of SSRF attack: accessing internal metadata service (e.g., AWS EC2)
# fetch_url_vulnerable("http://169.254.169.254/latest/meta-data/")

# Example of fetching an external URL with disabled SSL verification
fetch_url_vulnerable("https://example.com")
```

Secure:
```python
import urllib.request
import ssl
import re

# Define a whitelist of allowed

---

Document Title: Bandit Python Security Rules — Detailed RAG Knowledge Base
Official Source: https://bandit.readthedocs.io/en/latest/

# 41. B501 — request_with_no_cert_validation

This rule identifies instances where the `requests` library is used to make HTTP requests without proper SSL certificate validation. When `verify=False` is passed to `requests.get()`, `requests.post()`, or similar methods, the client will not verify the authenticity of the server's SSL certificate. This means that an attacker performing a Man-in-the-Middle (MitM) attack can intercept, read, and modify traffic between the client and the server without the client detecting anything suspicious. This compromises the confidentiality and integrity of the communication, making it a critical security vulnerability, especially when dealing with sensitive data like credentials, personal information, or financial transactions. Disabling certificate validation bypasses a fundamental security mechanism designed to ensure you are communicating with the intended server.

```text
Review Checks:
- Identify calls to `requests.get`, `requests.post`, `requests.put`, `requests.delete`, `requests.head`, `requests.options`, `requests.request`.
- Check for the presence and value of the `verify` argument.
- Flag `verify=False` explicitly.
- Flag absence of `verify` argument if a global setting or environment variable might disable it (though Bandit primarily flags explicit `False`).
- Consider `urllib3.disable_warnings(InsecureRequestWarning)` as a related indicator.
```

Vulnerable:
```python
import requests
import urllib3

# This explicitly disables certificate verification, making the connection vulnerable to MitM attacks.
response = requests.get('https://example.com/api/data', verify=False)
print(f"Status Code: {response.status_code}")

# Another common pattern that indicates disabled verification
session = requests.Session()
session.verify = False
response = session.post('https://secure.internal.app/submit', json={'data': 'sensitive'})
print(f"Session Status Code: {response.status_code}")

# Suppressing warnings often accompanies disabled verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
response = requests.get('https://another-example.com/info', verify=False)
print(f"Warning Suppressed Status Code: {response.status_code}")
```

Secure:
```python
import requests
import certifi # Recommended for bundling CA certificates

# By default, requests verifies SSL certificates. Explicitly setting verify=True is good practice.
# Ensure your system's CA certificate store is up-to-date or specify a trusted CA bundle.
try:
    response = requests.get('https://example.com/api/data', verify=True)
    response.raise_for_status() # Raise an exception for HTTP errors
    print(f"Status Code: {response.status_code}")
except requests.exceptions.SSLError as e:
    print(f"SSL Certificate Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")

# Using a session with default (enabled) verification
session = requests.Session()
# session.verify defaults to True, no need to set it explicitly unless overriding
response = session.post('https://secure.internal.app/submit', json={'data': 'sensitive'})
response.raise_for_status()
print(f"Session Status Code: {response.status_code}")

# If a custom CA bundle is required (e.g., for internal services with self-signed certs)
# Ensure 'path/to/your/custom_ca_bundle.pem' is a trusted and secure file.
try:
    response = requests.get('https://internal-service.com/status', verify='/etc/ssl/certs/custom_ca_bundle.pem')
    response.raise_for_status()
    print(f"Custom CA Status Code: {response.status_code}")
except requests.exceptions.SSLError as e:
    print(f"Custom CA SSL Error: {e}")
```

Assistant Behavior:
The AI code reviewer should report this issue as a High severity vulnerability. The report must clearly state that disabling SSL certificate validation exposes the application to Man-in-the-Middle (MitM) attacks, compromising data confidentiality and integrity. It should explain that an attacker could intercept and tamper with communication, potentially leading to data theft, unauthorized access, or execution of malicious code. The remediation guidance should emphasize removing `verify=False` and ensuring that `requests` uses its default behavior of validating certificates against a trusted CA store. If self-signed certificates are used in a controlled environment, the AI should recommend providing a path to a trusted custom CA bundle (`verify='/path/to/cert.pem'`) rather than disabling verification entirely. It should also advise against suppressing `InsecureRequestWarning` without addressing the underlying cause.

---

# 42. B502 — ssl_with_bad_version

This rule flags the use of outdated or insecure SSL/TLS protocol versions. Specifying an older protocol version like SSLv2, SSLv3, or even older TLSv1.0/TLSv1.1 explicitly makes the communication vulnerable to known cryptographic attacks. These older protocols have documented weaknesses, such as POODLE (SSLv3), BEAST (TLSv1.0), and various other vulnerabilities that allow attackers to decrypt sensitive information, forge messages, or downgrade connections to weaker ciphers. Modern applications should exclusively use TLSv1.2 or TLSv1.3, which incorporate stronger cryptographic algorithms and better security practices. Hardcoding an insecure version prevents the system from automatically negotiating the strongest available protocol, thereby introducing a critical security flaw.

```text
Review Checks:
- Identify `ssl.wrap_socket` calls or `ssl.SSLContext` instantiation.
- Check the `ssl_version` or `minimum_version` argument.
- Flag `ssl.PROTOCOL_SSLv2`, `ssl.PROTOCOL_SSLv3`, `ssl.PROTOCOL_TLSv1`, `ssl.PROTOCOL_TLSv1_1`.
- Flag `ssl.PROTOCOL_SSLv23` if not properly configured to exclude older versions.
- Recommend `ssl.PROTOCOL_TLSv1_2` or `ssl.PROTOCOL_TLSv1_3` (or `ssl.PROTOCOL_TLS_SERVER`/`ssl.PROTOCOL_TLS_CLIENT` for modern defaults).
```

Vulnerable:
```python
import ssl
import socket

# Using an outdated and insecure SSLv3 protocol version
# This is highly vulnerable to attacks like POODLE.
context_v3 = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
context_v3.verify_mode = ssl.CERT_REQUIRED
context_v3.load_verify_locations("ca_cert.pem")
# Attempting to create a socket with this context
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ssl_sock = context_v3.wrap_socket(s, server_hostname='example.com')

# Using TLSv1.0, which has known vulnerabilities like BEAST
context_tls1_0 = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context_tls1_0.verify_mode = ssl.CERT_REQUIRED
context_tls1_0.load_verify_locations("ca_cert.pem")

# Using SSLv23 without explicit minimum version setting can allow negotiation down to insecure versions
# This is problematic if not properly restricted.
context_v23 = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context_v23.verify_mode = ssl.CERT_REQUIRED
context_v23.load_verify_locations("ca_cert.pem")
```

Secure:
```python
import ssl
import socket

# Always use the highest available secure protocol version.
# ssl.PROTOCOL_TLS_CLIENT and ssl.PROTOCOL_TLS_SERVER are preferred for modern defaults.
# They automatically select the highest secure protocol version available (TLSv1.2 or TLSv1.3).
context_client = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context_client.verify_mode = ssl.CERT_REQUIRED
context_client.load_verify_locations("ca_cert.pem")
context_client.minimum_version = ssl.TLSVersion.TLSv1_2 # Explicitly set minimum to TLSv1.2 or higher
context_client.set_ciphers('HIGH:!aNULL:!MD5:!RC4:!DES:!3DES:!DSS:!PSK:!SRP:!EXP:!LOW:@STRENGTH') # Strong cipher suite

# For server-side contexts, use PROTOCOL_TLS_SERVER
context_server = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context_server.verify_mode = ssl.CERT_REQUIRED # For client cert verification if needed
context_server.load_cert_chain("server_cert.pem", "server_key.pem")
context_server.minimum_version = ssl.TLSVersion.TLSv1_2
context_server.set_ciphers('HIGH:!aNULL:!MD5:!RC4:!DES:!3DES:!DSS:!PSK:!SRP:!EXP:!LOW:@STRENGTH')

# Example of using TLSv1.2 explicitly if TLSv1.3 is not yet universally supported or desired
context_tls1_2 = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context_tls1_2.verify_mode = ssl.CERT_REQUIRED
context_tls1_2.load_verify_locations("ca_cert.pem")
context_tls1_2.set_ciphers('HIGH:!aNULL:!MD5:!RC4:!DES:!3DES:!DSS:!PSK:!SRP:!EXP:!LOW:@STRENGTH')

# Example usage (conceptual, actual socket handling omitted for brevity)
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ssl_sock = context_client.wrap_socket(s, server_hostname='example.com')
```

Assistant Behavior:
The AI code reviewer should flag this as a Critical severity issue. It should explain that using outdated SSL/TLS protocol versions (like SSLv2, SSLv3, TLSv1.0, TLSv1.1) exposes the application to well-known cryptographic attacks, leading to potential data decryption, tampering, or session hijacking. The report should emphasize that these protocols have severe vulnerabilities that have been exploited in the past. Remediation should instruct the developer to update the `ssl.SSLContext` instantiation to use `ssl.PROTOCOL_TLS_CLIENT` or `ssl.PROTOCOL_TLS_SERVER` (for modern Python versions) or explicitly set `minimum_version` to `ssl.TLSVersion.TLSv1_2` or higher. It should also recommend configuring strong cipher suites and keeping the `ssl` library and underlying OpenSSL updated.

---

# 43. B503 — ssl_with_bad_defaults

This rule targets the use of `ssl.SSLContext` with insecure default settings, particularly when `ssl.PROTOCOL_SSLv23` is used without further restrictions. While `ssl.PROTOCOL_SSLv23` (or `ssl.PROTOCOL_TLS`) is designed to negotiate the highest common protocol version, it can still allow negotiation down to insecure versions (like TLSv1.0 or TLSv1.1, or even SSLv3 if not explicitly disabled by the underlying OpenSSL configuration) if the server or client supports them. This creates a downgrade attack vector. Furthermore, `ssl.SSLContext` objects, by default, might not have the most secure options enabled (e.g., `OP_NO_SSLv2`, `OP_NO_SSLv3`, `OP_NO_TLSv1`, `OP_NO_TLSv1_1`, or `OP_NO_COMPRESSION`). Failing to explicitly configure these options or set a minimum TLS version can lead to a less secure connection than intended, making it susceptible to various cryptographic attacks.

```text
Review Checks:
- Identify `ssl.SSLContext` instantiation, especially with `ssl.PROTOCOL_SSLv23` or `ssl.PROTOCOL_TLS`.
- Check if `minimum_version` is set to `ssl.TLSVersion.TLSv1_2` or higher.
- Check if `options` are explicitly set to disable insecure protocols (e.g., `context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1`).
- Verify that a strong cipher suite is configured using `context.set_ciphers()`.
```

Vulnerable:
```python
import ssl
import socket

# Using SSLv23 without explicitly setting minimum version or disabling insecure options.
# This can allow negotiation down to TLSv1.0/1.1 or even SSLv3 if the peer supports it.
context_bad_defaults = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context_bad_defaults.verify_mode = ssl.CERT_REQUIRED
context_bad_defaults.load_verify_locations("ca_cert.pem")
# No explicit minimum_version set, no insecure options disabled.
# This context is susceptible to downgrade attacks.

# Another example, relying on system defaults which might not be hardened
context_generic = ssl.create_default_context()
# While create_default_context is generally better, it might still allow TLSv1.0/1.1
# depending on Python version and underlying OpenSSL configuration.
# It's safer to explicitly set minimum_version.
```

Secure:
```python
import ssl
import socket

# Preferred: Use PROTOCOL_TLS_CLIENT/SERVER and set minimum_version.
# These protocols automatically disable older SSL/TLS versions and enable secure options.
context_secure = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context_secure.verify_mode = ssl.CERT_REQUIRED
context_secure.load_verify_locations("ca_cert.pem")
context_secure.minimum_version = ssl.TLSVersion.TLSv1_2 # Enforce TLSv1.2 or higher
# Explicitly set secure options, though minimum_version often handles this for modern protocols.
context_secure.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
context_secure.options |= ssl.OP_NO_COMPRESSION # Disable compression to prevent CRIME/BREACH attacks
context_secure.set_ciphers('HIGH:!aNULL:!MD5:!RC4:!DES:!3DES:!DSS:!PSK:!SRP:!EXP:!LOW:@STRENGTH') # Strong cipher suite

# For server-side context
context_server_secure = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context_server_secure.load_cert_chain("server_cert.pem", "server_key.pem")
context_server_secure.minimum_version = ssl.TLSVersion.TLSv1_2
context_server_secure.options |= ssl.OP_NO_COMPRESSION
context_server_secure.set_ciphers('HIGH:!aNULL:!MD5:!RC4:!DES:!3DES:!DSS:!PSK:!SRP:!EXP:!LOW:@STRENGTH')

# If using ssl.create_default_context(), always customize it for security
context_default_hardened = ssl.create_default_context()
context_default_hardened.minimum_version = ssl.TLSVersion.TLSv1_2
context_default_hardened.set_ciphers('HIGH:!aNULL:!MD5:!RC4:!DES:!3DES:!DSS:!PSK:!SRP:!EXP:!LOW:@STRENGTH')
```

Assistant Behavior:
The AI code reviewer should report this as a High severity vulnerability. It should explain that relying on insecure default settings for `ssl.SSLContext` or using `ssl.PROTOCOL_SSLv23` without proper restrictions can lead to downgrade attacks, where an attacker forces the connection to use an older, vulnerable protocol version (like TLSv1.0/1.1 or SSLv3). This compromises the confidentiality and integrity of the communication. The remediation steps should include explicitly setting `ssl.SSLContext.minimum_version` to `ssl.TLSVersion.TLSv1_2` or higher, or using `ssl.PROTOCOL_TLS_CLIENT`/`ssl.PROTOCOL_TLS_SERVER` for modern Python versions. It should also recommend explicitly disabling insecure options like `ssl.OP_NO_SSLv2`, `ssl.OP_NO_SSLv3`, `ssl.OP_NO_TLSv1`, `ssl.OP_NO_TLSv1_1`, and `ssl.OP_NO_COMPRESSION`, and configuring a strong, modern cipher suite.

---

# 44. B504 — ssl_with_no_version

This rule flags the instantiation of `ssl.SSLContext` without explicitly specifying a protocol version or using `ssl.PROTOCOL_TLS` (which is an alias for `ssl.PROTOCOL_SSLv23` in older Python versions). While `ssl.PROTOCOL_TLS` is intended to negotiate the highest common protocol, simply omitting the `protocol` argument or relying on `ssl.PROTOCOL_SSLv23` without further hardening can lead to the use of insecure or outdated TLS versions if the underlying system's OpenSSL configuration or the peer's capabilities allow it. This is similar to B503 but specifically targets the lack of explicit version control. The risk is that the application might inadvertently negotiate an older, vulnerable protocol (e.g., TLSv1.0 or TLSv1.1) that has known cryptographic weaknesses, making the communication susceptible to downgrade attacks and other exploits.

```text
Review Checks:
- Identify `ssl.SSLContext()` calls.
- Check if the `protocol` argument is missing or set to `None`.
- Check if `protocol` is explicitly set to `ssl.PROTOCOL_SSLv23` or `ssl.PROTOCOL_TLS` (without `minimum_version` or `options` hardening).
- Verify that `minimum_version` is set to `ssl.TLSVersion.TLSv1_2` or higher.
```

Vulnerable:
```python
import ssl
import socket

# Instantiating SSLContext without specifying a protocol version.
# This implicitly uses ssl.PROTOCOL_TLS (or SSLv23), which can be insecure without further configuration.
context_no_version = ssl.SSLContext()
context_no_version.verify_mode = ssl.CERT_REQUIRED
context_no_version.load_verify_locations("ca_cert.pem")
# This context might negotiate an insecure TLS version if not explicitly restricted.

# Explicitly using PROTOCOL_TLS (alias for SSLv23) without hardening
context_tls_unhardened = ssl.SSLContext(ssl.PROTOCOL_TLS)
context_tls_unhardened.verify_mode = ssl.CERT_REQUIRED
context_tls_unhardened.load_verify_locations("ca_cert.pem")
# This is also vulnerable to downgrade attacks.
```

Secure:
```python
import ssl
import socket

# Preferred: Use PROTOCOL_TLS_CLIENT/SERVER and set minimum_version.
# These automatically provide secure defaults and disable older protocols.
context_secure_client = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context_secure_client.verify_mode = ssl.CERT_REQUIRED
context_secure_client.load_verify_locations("ca_cert.pem")
context_secure_client.minimum_version = ssl.TLSVersion.TLSv1_2 # Enforce TLSv1.2 or higher
context_secure_client.set_ciphers('HIGH:!aNULL:!MD5:!RC4:!DES:!3DES:!DSS:!PSK:!SRP:!EXP:!LOW:@STRENGTH')

# For server-side context
context_secure_server = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context_secure_server.load_cert_chain("server_cert.pem", "server_key.pem")
context_secure_server.minimum_version = ssl.TLSVersion.TLSv1_2
context_secure_server.set_ciphers('HIGH:!aNULL:!MD5:!RC4:!DES:!3DES:!DSS:!PSK:!SRP:!EXP:!LOW:@STRENGTH')

# If using ssl.create_default_context(), always customize it for security
context_default_hardened = ssl.create_default_context()
context_default_hardened.minimum_version = ssl.TLSVersion.TLSv1_2
context_default_hardened.set_ciphers('HIGH:!aNULL:!MD5:!RC4:!DES:!3DES:!DSS:!PSK:!SRP:!EXP:!LOW:@STRENGTH')
```

Assistant Behavior:
The AI code reviewer should report this as a High severity vulnerability. It should explain that instantiating `ssl.SSLContext` without explicitly defining a secure protocol version or hardening the default `ssl.PROTOCOL_TLS` (or `ssl.PROTOCOL_SSLv23`) can lead to the negotiation of outdated and vulnerable TLS versions (e.g., TLSv1.0/1.1). This exposes the application to downgrade attacks and other known cryptographic weaknesses, compromising the confidentiality and integrity of data in transit. The remediation guidance should instruct the developer to use `ssl.PROTOCOL_TLS_CLIENT` or `ssl.PROTOCOL_TLS_SERVER` (for Python 3.6+) and, crucially, to set `ssl.SSLContext.minimum_version` to `ssl.TLSVersion.TLSv1_2` or higher. It should also recommend configuring a strong cipher suite to ensure robust cryptographic protection.

---

# 45. B505 — weak_cryptographic_key

This rule identifies the use of weak cryptographic keys, specifically when generating RSA keys with a key size less than 2048 bits. For modern security standards, RSA keys shorter than 2048 bits are considered cryptographically weak and can be brute-forced by attackers with sufficient computational resources. A 1024-bit RSA key, for example, can be factored within a reasonable timeframe using specialized hardware or cloud computing, compromising the security of any data encrypted or signed with that key. This vulnerability directly impacts the confidentiality, integrity, and authenticity of cryptographic operations, making it possible for attackers to decrypt sensitive data, forge digital signatures, or impersonate legitimate entities. Strong cryptographic keys are fundamental to robust security.

```text
Review Checks:
- Identify calls to `cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key`.
- Check the `key_size` argument.
- Flag `key_size` values less than 2048.
- Consider other key generation functions if they allow specifying key size (e.g., `OpenSSL.crypto.PKey.generate_key`).
```

Vulnerable:
```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Generating an RSA key with a weak key size (1024 bits)
# This key is susceptible to brute-force attacks.
private_key_weak = rsa.generate_private_key(
    public_exponent=65537,
    key_size=1024, # Vulnerable: Key size is too small
    backend=default_backend()
)

# Serializing for demonstration (not the vulnerability itself)
pem_weak = private_key_weak.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
print(f"Weak Key PEM (first 50 chars): {pem_weak.decode()[:50]}...")
```

Secure:
```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Generating an RSA key with a strong key size (2048 bits or higher)
# 2048 bits is the current minimum recommended for general use.
# 3072 or 4096 bits are even better for long-term security.
private_key_secure = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048, # Secure: Key size is 2048 bits or more
    backend=default_backend()
)

# Serializing for demonstration
pem_secure = private_key_secure.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(b'strong-password') # Always encrypt private keys
)
print(f"Secure Key PEM (first 50 chars): {pem_secure.decode()[:50]}...")

# Example with an even stronger key size
private_key_stronger = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096, # Even more secure
    backend=default_backend()
)
```

Assistant Behavior:
The AI code reviewer should report this as a High severity vulnerability. It should explain that generating RSA cryptographic keys with a key size less than 2048 bits renders them weak and susceptible to brute-force attacks, compromising the confidentiality and integrity of encrypted data and the authenticity of digital signatures. It should emphasize that attackers with sufficient computational resources could decrypt sensitive information or forge identities. The remediation guidance should instruct the developer to increase the `key_size` parameter to at least 2048 bits, with 3072 or 4096 bits being preferred for long-term security. Additionally, it should recommend securely storing private keys, ideally encrypted with a strong passphrase, and regularly reviewing key management practices.

---

# 46. B506 — yaml_load

This rule flags the use of `yaml.load()` without specifying a safe loader, which is a critical security vulnerability. The `yaml.load()` function, by default, can parse and execute arbitrary Python objects from a YAML string. This means that if an attacker can supply a malicious YAML payload to an application that uses `yaml.load()`, they can achieve arbitrary code execution on the server. This is a severe remote code execution (RCE) vulnerability that can lead to complete system compromise, data exfiltration, or denial of service. The `yaml.safe_load()` function should always be used instead, as it restricts the deserialization to basic YAML types, preventing the execution of arbitrary code.

```text
Review Checks:
- Identify calls to `yaml.load`.
- Check if `Loader` argument is explicitly set to `yaml.SafeLoader`.
- Flag `yaml.load(data)` without a `Loader` argument.
- Flag `yaml.load(data, Loader=yaml.UnsafeLoader)` (though `UnsafeLoader` is not a standard PyYAML class, it's a conceptual flag).
```

Vulnerable:
```python
import yaml
import os

# This is a critical vulnerability: yaml.load() without a specified Loader
# allows arbitrary code execution if a malicious YAML string is provided.
malicious_yaml_payload = """
!!python/object/apply:os.system ["echo PWNED! && ls -la /"]
"""

print("Attempting to load malicious YAML with vulnerable yaml.load()...")
try:
    # If this code were run, it would execute the os.system command.
    # For safety, we'll just show the vulnerable call.
    # yaml.load(malicious_yaml_payload)
    print("Vulnerable call: yaml.load(malicious_yaml_payload)")
    config_data_vulnerable = yaml.load("{'user': 'admin', 'password': 'password123'}")
    print(f"Loaded (vulnerable): {config_data_vulnerable}")
except Exception as e:
    print(f"Error during vulnerable load (expected for actual execution): {e}")

# Another example with a simple configuration
user_input_config = "name: John Doe\nage: 30"
# If this came from an untrusted source, it's dangerous.
# config = yaml.load(user_input_config)
```

Secure:
```python
import yaml
import os

# Always use yaml.safe_load() to prevent arbitrary code execution.
# This limits deserialization to basic YAML types (strings, numbers, lists, dicts).
malicious_yaml_payload = """
!!python/object/apply:os.system ["echo PWNED! && ls -la /"]
"""

print("Attempting to load malicious YAML with secure yaml.safe_load()...")
try:
    # This will raise a YAMLError because it tries to load an unsafe object.
    # config_data_secure = yaml.safe_load(malicious_yaml_payload)
    # print(f"Loaded (secure): {config_data_secure}")
    print("Secure call: yaml.safe_load(malicious_yaml_payload) will prevent execution.")
    config_data_secure = yaml.safe_load("{'user': 'admin', 'password': 'password123'}")
    print(f"Loaded (secure): {config_data_secure}")
except yaml.YAMLError as e:
    print(f"Successfully prevented unsafe YAML load: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

# Loading a legitimate configuration from a trusted source
trusted_config = "database:\n  host: localhost\n  port: 5432"
config = yaml.safe_load(trusted_config)
print(f"Loaded trusted config: {config}")
```

Assistant Behavior:
The AI code reviewer should report this as a Critical severity vulnerability, specifically categorizing it as Remote Code Execution (RCE). It must clearly explain that using `yaml.load()` without `yaml.SafeLoader` allows an attacker to execute arbitrary code on the server by supplying a specially crafted malicious YAML payload. This can lead to complete system compromise. The remediation guidance should be unequivocal: replace all instances of `yaml.load()` with `yaml.safe_load()`. The report should also advise developers to treat all external input as untrusted and to validate and sanitize it thoroughly before processing, even with `safe_load`, to prevent other forms of data manipulation or denial of service.

---

# 47. B507 — ssh_no_host_key_verification

This rule detects instances where SSH client libraries

---

