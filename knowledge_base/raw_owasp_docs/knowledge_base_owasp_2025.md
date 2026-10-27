# OWASP Top 10:2025 — Detailed RAG Knowledge Base

> Consolidated RAG reference document for the AI Security Analysis Agent.

---

## Section 1: 0X00 2025-Introduction

![OWASP Logo](../assets/TOP_10_logo_Final_Logo_Colour.png)

# The Ten Most Critical Web Application Security Risks

# Introduction

Welcome to the 8th installment of the OWASP Top Ten! 

A huge thank you to everyone who contributed data and perspectives in the survey. Without you, this installment would not have been possible. **THANK YOU!**


## Introducing the OWASP Top 10:2025



* [A01:2025 - Broken Access Control](A01_2025-Broken_Access_Control.md)
* [A02:2025 - Security Misconfiguration](A02_2025-Security_Misconfiguration.md)
* [A03:2025 - Software Supply Chain Failures](A03_2025-Software_Supply_Chain_Failures.md)
* [A04:2025 - Cryptographic Failures](A04_2025-Cryptographic_Failures.md)
* [A05:2025 - Injection](A05_2025-Injection.md)
* [A06:2025 - Insecure Design](A06_2025-Insecure_Design.md)
* [A07:2025 - Authentication Failures](A07_2025-Authentication_Failures.md)
* [A08:2025 - Software or Data Integrity Failures](A08_2025-Software_or_Data_Integrity_Failures.md)
* [A09:2025 - Security Logging & Alerting Failures](A09_2025-Security_Logging_and_Alerting_Failures.md)
* [A10:2025 - Mishandling of Exceptional Conditions](A10_2025-Mishandling_of_Exceptional_Conditions.md)


## What's changed in the Top 10 for 2025

There are two new categories and one consolidation in the Top Ten for 2025. We’ve worked to maintain our focus on the root cause over the symptoms as much as possible. With the complexity of software engineering and software security, it’s basically impossible to create ten categories without some level of overlap.

![Mapping](../assets/2025-mappings.png)

* **[A01:2025 - Broken Access Control](A01_2025-Broken_Access_Control.md)** maintains its position at #1 as the most serious application security risk; the contributed data indicates that on average, 3.73% of applications tested had one or more of the 40 Common Weakness Enumerations (CWEs) in this category. As indicated by the dashed line in the above figure, Server-Side Request Forgery (SSRF) has been rolled into this category.
* **[A02:2025 - Security Misconfiguration](A02_2025-Security_Misconfiguration.md)** moved up from #5 in 2021 to #2 in 2025. Misconfigurations are more prevalent in the data for this cycle. 3.00% of the applications tested had one or more of the 16 CWEs in this category. This is not surprising, as software engineering is continuing to increase the amount of an application’s behavior that is based on configurations.
* **[A03:2025 - Software Supply Chain Failures](A03_2025-Software_Supply_Chain_Failures.md)** is an expansion of [A06:2021-Vulnerable and Outdated Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/) to include a broader scope of compromises occurring within or across the entire ecosystem of software dependencies, build systems, and distribution infrastructure. This category was overwhelmingly voted a top concern in the community survey. This category has 5 CWEs and a limited presence in the collected data, but we believe this is due to challenges in testing and hope that testing catches up in this area. This category has the fewest occurrences in the data, but also the highest average exploit and impact scores from CVEs.
* **[A04:2025 - Cryptographic Failures](A04_2025-Cryptographic_Failures.md)** falls two spots from #2 to #4 in the ranking. The contributed data indicates that, on average, 3.80% of applications have one or more of the 32 CWEs in this category. This category often leads to sensitive data exposure or system compromise.
* **[A05:2025 - Injection](A05_2025-Injection.md)** falls two spots from #3 to #5 in the ranking, maintaining its position relative to Cryptographic Failures and Insecure Design. Injection is one of the most tested categories, with the greatest number of CVEs associated with the 38 CWEs in this category. Injection includes a range of issues from Cross-site Scripting (high frequency/low impact) to SQL Injection (low frequency/high impact) vulnerabilities.
* **[A06:2025 - Insecure Design](A06_2025-Insecure_Design.md)** slides two spots from #4 to #6 in the ranking as Security Misconfiguration and Software Supply Chain Failures leapfrog it. This category was introduced in 2021, and we have seen noticeable improvements in the industry related to threat modeling and a greater emphasis on secure design.
* **[A07:2025 - Authentication Failures](A07_2025-Authentication_Failures.md)** maintains its position at #7 with a slight name change (prevously it was “[Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)") to more accurately reflect the 36 CWEs in this category. This category remains important, but the increased use of standardized frameworks for authentication appears to be having beneficial effects on the occurrences of authentication failures.
* **[A08:2025 - Software or Data Integrity Failures](A08_2025-Software_or_Data_Integrity_Failures.md)** continues at #8 in the list. This category is focused on the failure to maintain trust boundaries and verify the integrity of software, code, and data artifacts at a lower level than Software Supply Chain Failures. 
* **[A09:2025 - Security Logging & Alerting Failures](A09_2025-Security_Logging_and_Alerting_Failures.md)** retains its position at #9. This category has a slight name change (previously [Security Logging and Monitoring Failures](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)”) to emphasize the importance of the alerting functionality needed to induce appropriate action on relevant logging events. Great logging with no alerting is of minimal value in identifying security incidents. This category will always be underrepresented in the data, and was again voted into a position in the list from the community survey participants.
* **[A10:2025 - Mishandling of Exceptional Conditions](A10_2025-Mishandling_of_Exceptional_Conditions.md)** is a new category for 2025. This category contains 24 CWEs focusing on improper error handling, logical errors, failing open, and other related scenarios stemming from abnormal conditions that systems may encounter.


## Methodology

This installment of the Top Ten remains data-informed, but not blindly data-driven. We ranked 12 categories based on the data contributed, and allowed two to be promoted or highlighted by responses from the community survey. We do this for a fundamental reason: examining the contributed data is essentially looking into the past. Application Security researchers dedicate time to identifying new vulnerabilities and developing new testing methods. It takes weeks to years to integrate these tests into tools and processes. By the time we can reliably test a weakness at scale, years may have passed. There are also important risks that we may never be able to reliably test and be present in the data. To balance that view, we use a community survey to ask application security and development practitioners on the front lines what they see as essential risks that may be underrepresented in the testing data.


## How the categories are structured

A few categories have changed from the previous installment of the OWASP Top Ten. Here is a high-level summary of the category changes.

In this iteration, we asked for data, with no restriction on CWEs like we did for the 2021 edition. We asked for the number of applications tested for a given year (starting in 2021), and the number of applications with at least one instance of a CWE found in testing. This format allows us to track how prevalent each CWE is within the population of applications. We ignore frequency for our purposes; while it may be necessary for other situations, it only hides the actual prevalence in the application population. Whether an application has four instances of a CWE or 4,000 instances is not part of the calculation for the Top Ten. Especially as manual testers tend to only list a vulnerability once no matter how many times it is repeated in an application, while automated testing frameworks list every instance of a vulnerability as unique. We went from approximately 30 CWEs in 2017, to almost 400 CWEs in 2021, to 589 CWEs in this edition to analyze in the dataset. We plan to do additional data analysis as a supplement in the future. This significant increase in the number of CWEs necessitates changes to how the categories are structured.

We spent several months grouping and categorizing CWEs and could have continued for additional months. We had to stop at some point. There are both root cause and symptom types of CWEs, where root cause types are like "Cryptographic Failure" and "Misconfiguration" contrasted to symptom types like "Sensitive Data Exposure" and "Denial of Service." We decided to focus on the root cause whenever possible as it's more logical for providing identification and remediation guidance. Focusing on the root cause over the symptom isn't a new concept; the Top Ten has been a mix of symptom and root cause. CWEs are also a mix of symptom and root cause; we are simply being more deliberate about calling it out. There is an average of 25 CWEs per category in this installment, with the lower bounds at 5 CWEs for A03:2025-Software Supply Chain Failures and A09:2025 Security Logging and Alerting Failures to 40 CWEs in A01:2025-Broken Access Control. We made the decision to cap the number of CWEs in a category to 40. This updated category structure offers additional training benefits as companies can focus on CWEs that make sense for a language/framework. 

We have been asked why not shift to a list of 10 CWEs as a Top 10, similar to the MITRE Top 25 Most Dangerous Software Weaknesses. There are two primary reasons why we use multiple CWEs in categories. First, not all CWEs exist in all programming languages or frameworks. This causes issues for tooling and training/awareness programs as part of the Top Ten may not be applicable. The second reason is that there are multiple CWEs for common vulnerabilities. For example, there are multiple CWEs for general Injection, Command Injection, Cross-site Scripting, Hardcoded Passwords, Lack of Validation, Buffer Overflows, Cleartext Storage of Sensitive Information, and many others. Depending on the organization or tester, different CWEs might be used. By using a category with multiple CWEs we can help raise the baseline and awareness of the different types of weaknesses that may occur under a common category name. In this edition of the Top Ten 2025, there are 248 CWEs within the 10 categories. There are a total of 968 CWEs in the [downloadable dictionary from MITRE](https://cwe.mitre.org) at the time of this release.


## How the data is used for selecting categories

Similar to what we did for the 2021 edition, we leveraged CVE data for *Exploitability *and *(Technical) Impact*. We downloaded OWASP Dependency Check and extracted the CVSS Exploit and Impact scores, grouping them by relevant CWEs listed with the CVEs. It took a fair bit of research and effort, as all the CVEs have CVSSv2 scores, but there are flaws in CVSSv2 that CVSSv3 should address. After a certain point in time, all CVEs are assigned a CVSSv3 score as well. Additionally, the scoring ranges and formulas were updated between CVSSv2 and CVSSv3.

In CVSSv2, both Exploit and (Technical) Impact could be up to 10.0, but the formula would knock them down to 60% for Exploit and 40% for Impact. In CVSSv3, the theoretical max was limited to 6.0 for Exploit and 4.0 for Impact. With the weighting considered, the Impact scoring shifted higher, almost a point and a half on average in CVSSv3, and exploitability moved nearly half a point lower on average.

There are approximately 175k records (up from 125k in 2021) of CVEs mapped to CWEs in the National Vulnerability Database (NVD), extracted from OWASP Dependency Check. Additionally, there are 643 unique CWEs mapped to CVEs (up from 241 in 2021). Within the nearly 220k CVEs that were extracted, 160k had CVSS v2 scores, 156k had CVSS v3 scores, and 6k had CVSS v4 scores. Many CVEs have multiple scores, which is why they total more than 220k.

For the Top Ten 2025, we calculated average exploit and impact scores in the following manner. We grouped all the CVEs with CVSS scores by CWE and weighted both exploit and impact scores by the percentage of the population that had CVSSv3, as well as the remaining population with CVSSv2 scores, to get an overall average. We mapped these averages to the CWEs in the dataset to use as Exploit and (Technical) Impact scoring for the other half of the risk equation.

Why not use CVSS v4.0, you may ask? That’s because the scoring algorithm was fundamentally changed, and it no longer easily provides the *Exploit* or *Impact* scores as CVSS v2 and CVSSv3 do. We will attempt to figure out a way to use CVSS v4.0 scoring for future versions of the Top Ten, but we were unable to determine a timely way to do so for the 2025 edition.


## Why we use a community survey

The results in the data are largely limited to what the industry can test for in an automated fashion. Talk to a seasoned AppSec professional, and they will tell you about stuff they find and trends they see that aren't yet in the data. It takes time for people to develop testing methodologies for certain vulnerability types and then more time for those tests to be automated and run against a large population of applications. Everything we find is looking back in the past and might be missing trends from the last year, which are not present in the data.

Therefore, we only pick eight of the ten categories from the data because it's incomplete. The other two categories are from the Top 10 community survey. It allows the practitioners on the front lines to vote for what they see as the highest risks that might not be in the data (and may never be expressed in data).


## Thank you to our data contributors

The following organizations (along with several anonymous donors) kindly donated data for over 2.8 millions applications to make this the largest and most comprehensive application security data set. Without you, this would not be possible.

* Accenture (Prague)
* Anonymous (multiple)
* Bugcrowd
* Contrast Security
* CryptoNet Labs
* Intuitor SoftTech Services
* Orca Security
* Probely
* Semgrep
* Sonar
* usd AG
* Veracode
* Wallarm

## Lead Authors
* Andrew van der Stock - X: [@vanderaj](https://x.com/vanderaj)
* Brian Glas - X: [@infosecdad](https://x.com/infosecdad)
* Neil Smithline - X: [@appsecneil](https://x.com/appsecneil)
* Tanya Janca - X: [@shehackspurple](https://x.com/shehackspurple)
* Torsten Gigler - Mastodon: [@torsten_gigler@infosec.exchange](https://infosec.exchange/@torsten_gigler)

## Log issues and pull requests

Please log any corrections or issues:

### Project links:
* [Homepage](https://owasp.org/www-project-top-ten/)
* [GitHub repository](https://github.com/OWASP/Top10)

---

## Section 2: A01 2025-Broken Access Control

#  A01:2025 Broken Access Control ![icon](../assets/TOP_10_Icons_Final_Broken_Access_Control.png){: style="height:80px;width:80px" align="right"}



## Background. 

Maintaining its position at #1 in the Top Ten, 100% of the applications tested were found to have some form of broken access control. Notable CWEs included are *CWE-200: Exposure of Sensitive Information to an Unauthorized Actor*, *CWE-201: Exposure of Sensitive Information Through Sent Data*, *CWE-918 Server-Side Request Forgery (SSRF)*, and *CWE-352: Cross-Site Request Forgery (CSRF)*. This category has the highest number of occurrences in the contributed data, and second highest number of related CVEs.


## Score table.


<table>
  <tr>
   <td>CWEs Mapped 
   </td>
   <td>Max Incidence Rate
   </td>
   <td>Avg Incidence Rate
   </td>
   <td>Max Coverage
   </td>
   <td>Avg Coverage
   </td>
   <td>Avg Weighted Exploit
   </td>
   <td>Avg Weighted Impact
   </td>
   <td>Total Occurrences
   </td>
   <td>Total CVEs
   </td>
  </tr>
  <tr>
   <td>40
   </td>
   <td>20.15%
   </td>
   <td>3.74%
   </td>
   <td>100.00%
   </td>
   <td>42.93%
   </td>
   <td>7.04
   </td>
   <td>3.84
   </td>
   <td>1,839,701
   </td>
   <td>32,654
   </td>
  </tr>
</table>



## Description. 

Access control enforces policy such that users cannot act outside of their intended permissions. Failures typically lead to unauthorized information disclosure, modification or destruction of all data, or performing a business function outside the user's limits. Common access control vulnerabilities include:



* Violation of the principle of least privilege, commonly known as deny by default, where access should only be granted for particular capabilities, roles, or users, but is available to anyone.
* Bypassing access control checks by modifying the URL (parameter tampering or force browsing), internal application state, or the HTML page, or by using an attack tool that modifies API requests.
* Permitting viewing or editing someone else's account by providing its unique identifier (insecure direct object references)
* An accessible API with missing access controls for POST, PUT, and DELETE.
* Elevation of privilege. Acting as a user without being logged in or or gaining privileges beyond those expected of the logged in user (e.g. admin access).
* Metadata manipulation, such as replaying or tampering with a JSON Web Token (JWT) access control token, a cookie or hidden field manipulated to elevate privileges, or abusing JWT invalidation.
* CORS misconfiguration allows API access from unauthorized or untrusted origins.
* Force browsing (guessing URLs) to authenticated pages as an unauthenticated user or to privileged pages as a standard user.


## How to prevent. 

Access control is only effective when implemented in trusted server-side code or serverless APIs, where the attacker cannot modify the access control check or metadata.



* Except for public resources, deny by default.
* Implement access control mechanisms once and reuse them throughout the application, including minimizing Cross-Origin Resource Sharing (CORS) usage.
* Model access controls should enforce record ownership rather than allowing users to create, read, update, or delete any record.
* Unique application business limit requirements should be enforced by domain models.
* Disable web server directory listing and ensure file metadata (e.g., .git) and backup files are not present within web roots.
* Log access control failures, alert admins when appropriate (e.g., repeated failures).
* Implement rate limits on API and controller access to minimize the harm from automated attack tooling.
* Stateful session identifiers should be invalidated on the server after logout. Stateless JWT tokens should be short-lived to minimize the window of opportunity for an attacker. For longer-lived JWTs, consider using refresh tokens and following OAuth standards to revoke access.
* Use well-established toolkits or patterns that provide simple, declarative access controls.

Developers and QA staff should include functional access control in their unit and integration tests.


## Example attack scenarios. 

**Scenario #1:** The application uses unverified data in an SQL call that is accessing account information:


```
pstmt.setString(1, request.getParameter("acct"));
ResultSet results = pstmt.executeQuery( );
```


An attacker can simply modify the browser's 'acct' parameter to send any desired account number. If not correctly verified, the attacker can access any user's account.


```
https://example.com/app/accountInfo?acct=notmyacct
```


**Scenario #2:** An attacker simply forces browsers to target URLs. Admin rights are required for access to the admin page.


```
https://example.com/app/getappInfo
https://example.com/app/admin_getappInfo
```


If an unauthenticated user can access either page, it's a flaw. If a non-admin can access the admin page, this is a flaw.

**Scenario #3:** An application puts all of their access control in their front-end. While the attacker cannot get to `https://example.com/app/admin_getappInfo` due to JavaScript code running in the browser, they can simply execute:


```
$ curl https://example.com/app/admin_getappInfo
```


from the command line.


## References.

* [OWASP Proactive Controls: C1: Implement Access Control](https://top10proactive.owasp.org/archive/2024/the-top-10/c1-accesscontrol/)
* [OWASP Application Security Verification Standard: V8 Authorization](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x17-V8-Authorization.md)
* [OWASP Testing Guide: Authorization Testing](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/README)
* [OWASP Cheat Sheet: Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
* [PortSwigger: Exploiting CORS misconfiguration](https://portswigger.net/blog/exploiting-cors-misconfigurations-for-bitcoins-and-bounties)
* [OAuth: Revoking Access](https://www.oauth.com/oauth2-servers/listing-authorizations/revoking-access/)


## List of Mapped CWEs

* [CWE-22 Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')](https://cwe.mitre.org/data/definitions/22.html)

* [CWE-23 Relative Path Traversal](https://cwe.mitre.org/data/definitions/23.html)

* [CWE-36 Absolute Path Traversal](https://cwe.mitre.org/data/definitions/36.html)

* [CWE-59 Improper Link Resolution Before File Access ('Link Following')](https://cwe.mitre.org/data/definitions/59.html)

* [CWE-61 UNIX Symbolic Link (Symlink) Following](https://cwe.mitre.org/data/definitions/61.html)

* [CWE-65 Windows Hard Link](https://cwe.mitre.org/data/definitions/65.html)

* [CWE-200 Exposure of Sensitive Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/200.html)

* [CWE-201 Exposure of Sensitive Information Through Sent Data](https://cwe.mitre.org/data/definitions/201.html)

* [CWE-219 Storage of File with Sensitive Data Under Web Root](https://cwe.mitre.org/data/definitions/219.html)

* [CWE-276 Incorrect Default Permissions](https://cwe.mitre.org/data/definitions/276.html)

* [CWE-281 Improper Preservation of Permissions](https://cwe.mitre.org/data/definitions/281.html)

* [CWE-282 Improper Ownership Management](https://cwe.mitre.org/data/definitions/282.html)

* [CWE-283 Unverified Ownership](https://cwe.mitre.org/data/definitions/283.html)

* [CWE-284 Improper Access Control](https://cwe.mitre.org/data/definitions/284.html)

* [CWE-285 Improper Authorization](https://cwe.mitre.org/data/definitions/285.html)

* [CWE-352 Cross-Site Request Forgery (CSRF)](https://cwe.mitre.org/data/definitions/352.html)

* [CWE-359 Exposure of Private Personal Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/359.html)

* [CWE-377 Insecure Temporary File](https://cwe.mitre.org/data/definitions/377.html)

* [CWE-379 Creation of Temporary File in Directory with Insecure Permissions](https://cwe.mitre.org/data/definitions/379.html)

* [CWE-402 Transmission of Private Resources into a New Sphere ('Resource Leak')](https://cwe.mitre.org/data/definitions/402.html)

* [CWE-424 Improper Protection of Alternate Path](https://cwe.mitre.org/data/definitions/424.html)

* [CWE-425 Direct Request ('Forced Browsing')](https://cwe.mitre.org/data/definitions/425.html)

* [CWE-441 Unintended Proxy or Intermediary ('Confused Deputy')](https://cwe.mitre.org/data/definitions/441.html)

* [CWE-497 Exposure of Sensitive System Information to an Unauthorized Control Sphere](https://cwe.mitre.org/data/definitions/497.html)

* [CWE-538 Insertion of Sensitive Information into Externally-Accessible File or Directory](https://cwe.mitre.org/data/definitions/538.html)

* [CWE-540 Inclusion of Sensitive Information in Source Code](https://cwe.mitre.org/data/definitions/540.html)

* [CWE-548 Exposure of Information Through Directory Listing](https://cwe.mitre.org/data/definitions/548.html)

* [CWE-552 Files or Directories Accessible to External Parties](https://cwe.mitre.org/data/definitions/552.html)

* [CWE-566 Authorization Bypass Through User-Controlled SQL Primary Key](https://cwe.mitre.org/data/definitions/566.html)

* [CWE-601 URL Redirection to Untrusted Site ('Open Redirect')](https://cwe.mitre.org/data/definitions/601.html)

* [CWE-615 Inclusion of Sensitive Information in Source Code Comments](https://cwe.mitre.org/data/definitions/615.html)

* [CWE-639 Authorization Bypass Through User-Controlled Key](https://cwe.mitre.org/data/definitions/639.html)

* [CWE-668 Exposure of Resource to Wrong Sphere](https://cwe.mitre.org/data/definitions/668.html)

* [CWE-732 Incorrect Permission Assignment for Critical Resource](https://cwe.mitre.org/data/definitions/732.html)

* [CWE-749 Exposed Dangerous Method or Function](https://cwe.mitre.org/data/definitions/749.html)

* [CWE-862 Missing Authorization](https://cwe.mitre.org/data/definitions/862.html)

* [CWE-863 Incorrect Authorization](https://cwe.mitre.org/data/definitions/863.html)

* [CWE-918 Server-Side Request Forgery (SSRF)](https://cwe.mitre.org/data/definitions/918.html)

* [CWE-922 Insecure Storage of Sensitive Information](https://cwe.mitre.org/data/definitions/922.html)

* [CWE-1275 Sensitive Cookie with Improper SameSite Attribute](https://cwe.mitre.org/data/definitions/1275.html)

---

## Section 3: A02 2025-Security Misconfiguration

# A02:2025 Security Misconfiguration ![icon](../assets/TOP_10_Icons_Final_Security_Misconfiguration.png){: style="height:80px;width:80px" align="right"}


## Background. 

Moving up from #5 in the previous edition, 100% of the applications tested were found to have some form of misconfiguration, with an average incidence rate of 3.00%, and over 719k occurrences of a Common Weakness Enumeration (CWE) in this risk category. With more shifts into highly configurable software, it's not surprising to see this category moving up. Notable CWEs included are *CWE-16 Configuration* and *CWE-611 Improper Restriction of XML External Entity Reference (XXE)*.


## Score table.


<table>
  <tr>
   <td>CWEs Mapped 
   </td>
   <td>Max Incidence Rate
   </td>
   <td>Avg Incidence Rate
   </td>
   <td>Max Coverage
   </td>
   <td>Avg Coverage
   </td>
   <td>Avg Weighted Exploit
   </td>
   <td>Avg Weighted Impact
   </td>
   <td>Total Occurrences
   </td>
   <td>Total CVEs
   </td>
  </tr>
  <tr>
   <td>16
   </td>
   <td>27.70%
   </td>
   <td>3.00%
   </td>
   <td>100.00%
   </td>
   <td>52.35%
   </td>
   <td>7.96
   </td>
   <td>3.97
   </td>
   <td>719,084
   </td>
   <td>1,375
   </td>
  </tr>
</table>



## Description. 

Security misconfiguration is when a system, application, or cloud service is set up incorrectly from a security perspective, creating vulnerabilities.

The application might be vulnerable if:



* It is missing appropriate security hardening across any part of the application stack or improperly configured permissions on cloud services.
* Unnecessary features are enabled or installed (e.g., unnecessary ports, services, pages, accounts, testing frameworks, or privileges).
* Default accounts and their passwords are still enabled and unchanged.
* A lack of central configuration for intercepting excessive error messages. Error handling reveals stack traces or other overly informative error messages to users.
* For upgraded systems, the latest security features are disabled or not configured securely.
* Excessive prioritization of backward compatibility leading to insecure configuration.
* The security settings in the application servers, application frameworks (e.g., Struts, Spring, ASP.NET), libraries, databases, etc., are not set to secure values.
* The server does not send security headers or directives, or they are not set to secure values.

Without a concerted, repeatable application security configuration hardening process, systems are at a higher risk.


## How to prevent. 

Secure installation processes should be implemented, including:



* A repeatable hardening process enabling the fast and easy deployment of another environment that is appropriately locked down. Development, QA, and production environments should all be configured identically, with different credentials used in each environment. This process should be automated to minimize the effort required to set up a new secure environment.
* A minimal platform without any unnecessary features, components, documentation, or samples. Remove or do not install unused features and frameworks.
* A task to review and update the configurations appropriate to all security notes, updates, and patches as part of the patch management process (see [A03 Software Supply Chain Failures](A03_2025-Software_Supply_Chain_Failures.md)). Review cloud storage permissions (e.g., S3 bucket permissions).
* A segmented application architecture provides effective and secure separation between components or tenants, with segmentation, containerization, or cloud security groups (ACLs).
* Sending security directives to clients, e.g., Security Headers.
* An automated process to verify the effectiveness of the configurations and settings in all environments.
* Proactively add a central configuration to intercept excessive error messages as a backup.
* If these verifications are not automated, they should be manually verified annually at a minimum.
* Use identity federation, short-lived credentials, or role-based access mechanisms provided by the underlying platform instead of embedding static keys or secrets in code, configuration files, or pipelines.


## Example attack scenarios. 

**Scenario #1:** The application server comes with sample applications not removed from the production server. These sample applications have known security flaws that attackers use to compromise the server. Suppose one of these applications is the admin console, and default accounts weren't changed. In that case, the attacker logs in with the default password and takes over.

**Scenario #2:** Directory listing is not disabled on the server. An attacker discovers they can simply list directories. The attacker finds and downloads the compiled Java classes, which they decompile and reverse engineer to view the code. The attacker then finds a severe access control flaw in the application.

**Scenario #3:** The application server's configuration allows detailed error messages, such as stack traces to be returned to users. This potentially exposes sensitive information or underlying flaws, such as component versions that are known to be vulnerable.

**Scenario #4:** A cloud service provider (CSP) defaults to having sharing permissions open to the Internet. This allows sensitive data stored within cloud storage to be accessed.


## References.

* [OWASP Testing Guide: Configuration Management](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/README)
* [OWASP Testing Guide: Testing for Error Codes](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/01-Testing_For_Improper_Error_Handling)
* [Application Security Verification Standard V13 Configuration](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x22-V13-Configuration.md)
* [NIST Guide to General Server Hardening](https://csrc.nist.gov/publications/detail/sp/800-123/final)
* [CIS Security Configuration Guides/Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
* [Amazon S3 Bucket Discovery and Enumeration](https://blog.websecurify.com/2017/10/aws-s3-bucket-discovery.html)
* ScienceDirect: Security Misconfiguration

## List of Mapped CWEs

* [CWE-5 J2EE Misconfiguration: Data Transmission Without Encryption](https://cwe.mitre.org/data/definitions/5.html)

* [CWE-11 ASP.NET Misconfiguration: Creating Debug Binary](https://cwe.mitre.org/data/definitions/11.html)

* [CWE-13 ASP.NET Misconfiguration: Password in Configuration File](https://cwe.mitre.org/data/definitions/13.html)

* [CWE-15 External Control of System or Configuration Setting](https://cwe.mitre.org/data/definitions/15.html)

* [CWE-16 Configuration](https://cwe.mitre.org/data/definitions/16.html)

* [CWE-260 Password in Configuration File](https://cwe.mitre.org/data/definitions/260.html)

* [CWE-315 Cleartext Storage of Sensitive Information in a Cookie](https://cwe.mitre.org/data/definitions/315.html)

* [CWE-489 Active Debug Code](https://cwe.mitre.org/data/definitions/489.html)

* [CWE-526 Exposure of Sensitive Information Through Environmental Variables](https://cwe.mitre.org/data/definitions/526.html)

* [CWE-547 Use of Hard-coded, Security-relevant Constants](https://cwe.mitre.org/data/definitions/547.html)

* [CWE-611 Improper Restriction of XML External Entity Reference](https://cwe.mitre.org/data/definitions/611.html)

* [CWE-614 Sensitive Cookie in HTTPS Session Without 'Secure' Attribute](https://cwe.mitre.org/data/definitions/614.html)

* [CWE-776 Improper Restriction of Recursive Entity References in DTDs ('XML Entity Expansion')](https://cwe.mitre.org/data/definitions/776.html)

* [CWE-942 Permissive Cross-domain Policy with Untrusted Domains](https://cwe.mitre.org/data/definitions/942.html)

* [CWE-1004 Sensitive Cookie Without 'HttpOnly' Flag](https://cwe.mitre.org/data/definitions/1004.html)

* [CWE-1174 ASP.NET Misconfiguration: Improper Model Validation](https://cwe.mitre.org/data/definitions/1174.html)

---

## Section 4: A03 2025-Software Supply Chain Failures

# A03:2025 Software Supply Chain Failures ![icon](../assets/TOP_10_Icons_Final_Vulnerable_Outdated_Components.png){: style="height:80px;width:80px" align="right"}


## Background.

This was top-ranked in the Top 10 community survey with exactly 50% respondents ranking it #1. Since initially appearing in the 2013 Top 10 as "A9 – Using Components with Known Vulnerabilities", the risk has grown in scope to include all supply chain failures, not just ones involving known vulnerabilities. Despite this increased scope, supply chain failures continue to be a challenge to identify with only 11 Common Vulnerability and Exposures (CVEs) having the related CWEs. However, when tested and reported in the contributed data, this category has the highest average incidence rate at 5.19%. The relevant CWEs are *CWE-477: Use of Obsolete Function, CWE-1104: Use of Unmaintained Third Party Components*, CWE-1329: *Reliance on Component That is Not Updateable*, and *CWE-1395: Dependency on Vulnerable Third-Party Component*.


## Score table.


<table>
  <tr>
   <td>CWEs Mapped
   </td>
   <td>Max Incidence Rate
   </td>
   <td>Avg Incidence Rate
   </td>
   <td>Max Coverage
   </td>
   <td>Avg Coverage
   </td>
   <td>Avg Weighted Exploit
   </td>
   <td>Avg Weighted Impact
   </td>
   <td>Total Occurrences
   </td>
   <td>Total CVEs
   </td>
  </tr>
  <tr>
   <td>6
   </td>
   <td>9.56%
   </td>
   <td>5.72%
   </td>
   <td>65.42%
   </td>
   <td>27.47%
   </td>
   <td>8.17
   </td>
   <td>5.23
   </td>
   <td>215,248
   </td>
   <td>11
   </td>
  </tr>
</table>



## Description.

Software supply chain failures are breakdowns or other compromises in the process of building, distributing, or updating software. They are often caused by vulnerabilities or malicious changes in third-party code, tools, or other dependencies that the system relies on.

You are likely vulnerable if:

* you do not carefully track the versions of all components that you use (both client-side and server-side). This includes components you directly use as well as nested (transitive) dependencies.
* the software is vulnerable, unsupported, or out of date. This includes the OS, web/application server, database management system (DBMS), applications, APIs and all components, runtime environments, and libraries.
* you do not scan for vulnerabilities regularly and subscribe to security bulletins related to the components you use.
* you do not have a change management process or tracking of changes within your supply chain, including tracking IDEs, IDE extensions and updates, changes to your organization's code repository, sandboxes, image and library repositories, the way artifacts are created and stored, etc. Every part of your supply chain should be documented, especially changes.
* you have not hardened every part of your supply chain, with a special focus on access control and the application of least privilege.
* your supply chain systems do not have any separation of duty. No single person should be able to write code and  promote it all the way to production without oversight from another human being.
* components from untrusted sources, across any part of the tech stack, are used in or can impact on production environments.
* you do not fix or upgrade the underlying platform, frameworks, and dependencies in a risk-based, timely fashion. This commonly happens in environments when patching is a monthly or quarterly task under change control, leaving organizations open to days or months of unnecessary exposure before fixing vulnerabilities.
* software developers do not test the compatibility of updated, upgraded, or patched libraries.
* you do not secure the configurations of every part of your system (see [A02:2025-Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/)).
* your CI/CD pipeline has weaker security than the systems it builds and deploys, especially if it is complex.


## How to prevent.

There should be a patch management process in place to:



* Centrally generate and manage the Software Bill of Materials (SBOM) of your entire software.
* Track not just your direct dependencies, but their (transitive) dependencies, and so on.
* Reduce attack surface by removing unused dependencies, unnecessary features, components, files, and documentation.
* Continuously inventory the versions of both client-side and server-side components (e.g., frameworks, libraries) and their dependencies using tools like OWASP Dependency Track, OWASP Dependency Check, retire.js, etc.
* Continuously monitor sources like Common Vulnerability and Exposures (CVE), National Vulnerability Database (NVD), and [Open Source Vulnerabilities (OSV)](https://osv.dev/) for vulnerabilities in the components you use. Use software composition analysis, software supply chain, or security-focused SBOM tools to automate the process. Subscribe to alerts for security vulnerabilities related to components you use.
* Only obtain components from official (trusted) sources over secure links. Prefer signed packages to reduce the chance of including a modified, malicious component (see [A08:2025-Software and Data Integrity Failures](https://owasp.org/Top10/2025/A08_2025-Software_or_Data_Integrity_Failures/)).
* Deliberately choose which version of a dependency you use and upgrade only when there is need.
* Monitor for libraries and components that are unmaintained or do not create security patches for older versions. If patching is not possible, consider migrating to an alternative. If that is not possible, consider deploying a virtual patch to monitor, detect, or protect against the discovered issue.
* Update your CI/CD, IDE, and any other developer tooling regularly
* Avoid deploying updates to all systems simultaneously. Use staged rollouts or canary deployments to limit exposure in case a trusted vendor is compromised.


There should be a change management process or tracking system in place to track changes to:

* CI/CD settings (all build tools and pipelines)
* Code repositories
* Sandbox areas
* Developer IDEs
* SBOM tooling, and created artifacts
* Logging systems and logs
* Third party integrations, such as SaaS
* Artifact repositories
* Container registries


Harden the following systems, which includes enabling MFA and locking down IAM:

* Your code repository (which includes not checking in secrets, protecting branches, backups)
* Developer workstations (regular patching, MFA, monitoring, and more)
* Your build server & CI/CD (separation of duties, access control, signed builds, environment-scoped secrets, tamper-evident logs, more)
* Your artifacts (ensure integrity via provenance, signing, and time stamping, promote artifacts rather than rebuilding for each environment, ensure builds are immutable)
* Infrastructure as code (managed like all code, including use of PRs and version control)

Every organization must ensure an ongoing plan for monitoring, triaging, and applying updates or configuration changes for the lifetime of the application or portfolio.


## Example attack scenarios.

**Scenario #1:** A trusted vendor is compromised with malware, leading to your computer systems being compromised when you upgrade. The most famous example of this is probably:



* The 2019 SolarWinds compromise that led to ~18,000 organizations being compromised. [https://www.npr.org/2021/04/16/985439655/a-worst-nightmare-cyberattack-the-untold-story-of-the-solarwinds-hack](https://www.npr.org/2021/04/16/985439655/a-worst-nightmare-cyberattack-the-untold-story-of-the-solarwinds-hack)

**Scenario #2:** A trusted vendor is compromised such that it behaves maliciously only under a specific condition.



* The 2025 Bybit theft of $1.5 billion was caused by [a supply chain attack in wallet software](https://www.sygnia.co/blog/sygnia-investigation-bybit-hack/) that only executed when the target wallet was being used.

**Scenario #3:** The [`Shai-Hulud` supply chain attack](https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem) in 2025 was the first successful self-propagating npm worm. Attacks seeded malicious versions of popular packages, which used a post-install script to harvest and exfiltrate sensitive data to public GitHub repositories. The malware would also detect npm tokens in the victim environment, and automatically use them to push malicious versions of any accessible package. The worm reached over 500 package versions before being disrupted by npm.  This supply chain attack was advanced, fast-spreading, and damaging, and by targeting developer machines it demonstrated developers themselves are now prime targets for supply chain attacks.

**Scenario #4:** Components typically run with the same privileges as the application itself, so flaws in any component can result in serious impact. Such flaws can be accidental (e.g., coding error) or intentional (e.g., a backdoor in a component). Some example exploitable component vulnerabilities discovered are:

* CVE-2017-5638, a Struts 2 remote code execution vulnerability that enables the execution of arbitrary code on the server, has been blamed for significant breaches.
* CVE-2021-44228 ("Log4Shell"), an Apache Log4j remote code execution zero-day vulnerability, has been blamed for ransomware, cryptomining, and other attack campaigns.


## References

* [OWASP Application Security Verification Standard: V15 Secure Coding and Architecture](https://owasp.org/www-project-application-security-verification-standard/)
* [OWASP Cheat Sheet Series: Dependency Graph SBOM](https://cheatsheetseries.owasp.org/cheatsheets/Dependency_Graph_SBOM_Cheat_Sheet.html)
* [OWASP Cheat Sheet Series: Vulnerable Dependency Management](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html)
* [OWASP Dependency-Track](https://owasp.org/www-project-dependency-track/)
* [OWASP CycloneDX](https://owasp.org/www-project-cyclonedx/)
* [OWASP Application Security Verification Standard: V1 Architecture, design and threat modelling](https://owasp-aasvs.readthedocs.io/en/latest/v1.html)
* [OWASP Dependency Check (for Java and .NET libraries)](https://owasp.org/www-project-dependency-check/)
* OWASP Testing Guide - Map Application Architecture (OTG-INFO-010)
* [OWASP Virtual Patching Best Practices](https://owasp.org/www-community/Virtual_Patching_Best_Practices)
* [The Unfortunate Reality of Insecure Libraries](https://www.scribd.com/document/105692739/JeffWilliamsPreso-Sm)
* [MITRE Common Vulnerabilities and Exposures (CVE) search](https://www.cve.org)
* [National Vulnerability Database (NVD)](https://nvd.nist.gov)
* [Retire.js for detecting known vulnerable JavaScript libraries](https://retirejs.github.io/retire.js/)
* [GitHub Advisory Database](https://github.com/advisories)
* Ruby Libraries Security Advisory Database and Tools
* [SAFECode Software Integrity Controls (PDF)](https://safecode.org/publication/SAFECode_Software_Integrity_Controls0610.pdf)
* [Glassworm supply chain attack](https://thehackernews.com/2025/10/self-spreading-glassworm-infects-vs.html)
* [PhantomRaven supply chain attack campaign](https://thehackernews.com/2025/10/phantomraven-malware-found-in-126-npm.html)


## List of Mapped CWEs

* [CWE-447 Use of Obsolete Function](https://cwe.mitre.org/data/definitions/447.html)

* [CWE-1035 2017 Top 10 A9: Using Components with Known Vulnerabilities](https://cwe.mitre.org/data/definitions/1035.html)

* [CWE-1104 Use of Unmaintained Third Party Components](https://cwe.mitre.org/data/definitions/1104.html)

* [CWE-1329 Reliance on Component That is Not Updateable](https://cwe.mitre.org/data/definitions/1329.html)

* [CWE-1357 Reliance on Insufficiently Trustworthy Component](https://cwe.mitre.org/data/definitions/1357.html)

* [CWE-1395 Dependency on Vulnerable Third-Party Component](https://cwe.mitre.org/data/definitions/1395.html)

---

## Section 5: A04 2025-Cryptographic Failures

# A04:2025 Cryptographic Failures ![icon](../assets/TOP_10_Icons_Final_Crypto_Failures.png){: style="height:80px;width:80px" align="right"}



## Background. 

Moving down two positions to #4, this weakness focuses on failures related to the lack of cryptography, insufficiently strong cryptography, leaking of cryptographic keys, and related errors. Three of the most common Common Weakness Enumerations (CWEs) in this risk involved the use of a weak pseudo-random number generator: *CWE-327 Use of a Broken or Risky Cryptographic Algorithm, CWE-331: Insufficient Entropy*, *CWE-1241: Use of Predictable Algorithm in Random Number Generator*, and *CWE-338 Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG)*.



## Score table.


<table>
  <tr>
   <td>CWEs Mapped 
   </td>
   <td>Max Incidence Rate
   </td>
   <td>Avg Incidence Rate
   </td>
   <td>Max Coverage
   </td>
   <td>Avg Coverage
   </td>
   <td>Avg Weighted Exploit
   </td>
   <td>Avg Weighted Impact
   </td>
   <td>Total Occurrences
   </td>
   <td>Total CVEs
   </td>
  </tr>
  <tr>
   <td>32
   </td>
   <td>13.77%
   </td>
   <td>3.80%
   </td>
   <td>100.00%
   </td>
   <td>47.74%
   </td>
   <td>7.23
   </td>
   <td>3.90
   </td>
   <td>1,665,348
   </td>
   <td>2,185
   </td>
  </tr>
</table>



## Description. 

Generally speaking, all data in transit should be encrypted at the [transport layer](https://en.wikipedia.org/wiki/Transport_layer) ([OSI layer](https://en.wikipedia.org/wiki/OSI_model) 4). Previous hurdles such as CPU performance and private key/certificate management are now handled by CPUs having instructions designed to accelerate encryption (eg: [AES support](https://en.wikipedia.org/wiki/AES_instruction_set)) and private key and certificate management being simplified by services like [LetsEncrypt.org](https://LetsEncrypt.org) with major cloud vendors providing even more tightly integrated certificate management services for their specific platforms. 

Beyond securing the transport layer, it is important to determine what data needs encryption at rest as well as what data needs extra encryption in transit (at the [application layer](https://en.wikipedia.org/wiki/Application_layer), OSI layer 7). For example, passwords, credit card numbers, health records, personal information, and business secrets require extra protection, especially if that data falls under privacy laws, e.g., EU's General Data Protection Regulation (GDPR), or regulations such as PCI Data Security Standard (PCI DSS). For all such data:



* Are any old or weak cryptographic algorithms or protocols used either by default or in older code?
* Are default crypto keys in use, are weak crypto keys generated, are keys re-used, or is proper key management and rotation missing? 
* Are crypto keys checked into source code repositories?
* Is encryption not enforced, e.g., are any HTTP headers (browser) security directives or headers missing?
* Is the received server certificate and the trust chain properly validated?
* Are initialization vectors ignored, reused, or not generated sufficiently secure for the cryptographic mode of operation? Is an insecure mode of operation such as ECB in use? Is encryption used when authenticated encryption is more appropriate?
* Are passwords being used as cryptographic keys in the absence of a password based key derivation function?
* Is randomness used that was not designed to meet cryptographic requirements? Even if the correct function is chosen, does it need to be seeded by the developer, and if not, has the developer over-written the strong seeding functionality built into it with a seed that lacks sufficient entropy/unpredictability?
* Are deprecated hash functions such as MD5 or SHA1 in use, or are non-cryptographic hash functions used when cryptographic hash functions are needed?
* Are cryptographic error messages or side channel information exploitable, for example in the form of padding oracle attacks?
* Can the cryptographic algorithm be downgraded or bypassed?

See references ASVS: Cryptography (V11), Secure Communication (V12) and Data Protection (V14).


## How to prevent. 

Do the following, at a minimum, and consult the references:



* Classify and label data processed, stored, or transmitted by an application. Identify which data is sensitive according to privacy laws, regulatory requirements, or business needs.
* Store your most sensitive keys in a hardware or cloud-based HSM.
* Use well-trusted implementations of cryptographic algorithms whenever possible.
* Don't store sensitive data unnecessarily. Discard it as soon as possible or use PCI DSS compliant tokenization or even truncation. Data that is not retained cannot be stolen.
* Make sure to encrypt all sensitive data at rest.
* Ensure up-to-date and strong standard algorithms, protocols, and keys are in place; use proper key management.
* Encrypt all data in transit with protocols >= TLS 1.2 only, with forward secrecy (FS) ciphers, drop support for cipher block chaining (CBC) ciphers, support quantum key change algorithms. For HTTPS enforce encryption using HTTP Strict Transport Security (HSTS). Check everything with a tool.
* Disable caching for responses that contain sensitive data. This includes caching in your CDN, web server, and any application caching (eg: Redis).
* Apply required security controls as per the data classification.
* Do not use unencrypted protocols such as FTP, and STARTTLS. Avoid using SMTP for transmitting confidential data.
* Store passwords using strong adaptive and salted hashing functions with a work factor (delay factor), such as Argon2, yescrypt, scrypt or PBKDF2-HMAC-SHA-512. For legacy systems using bcrypt, get more advice at [OWASP Cheat Sheet: Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
* Initialization vectors must be chosen appropriate for the mode of operation. This could mean using a CSPRNG (cryptographically secure pseudo random number generator). For modes that require a nonce, the initialization vector (IV) does not need a CSPRNG. In all cases, the IV should never be used twice for a fixed key.
* Always use authenticated encryption instead of just encryption.
* Keys should be generated cryptographically randomly and stored in memory as byte arrays. If a password is used, then it must be converted to a key via an appropriate password base key derivation function.
* Ensure that cryptographic randomness is used where appropriate and that it has not been seeded in a predictable way or with low entropy. Most modern APIs do not require the developer to seed the CSPRNG to be secure.
* Avoid deprecated cryptographic functions, block building methods and padding schemes, such as MD5, SHA1, Cipher Block Chaining Mode (CBC), PKCS number 1 v1.5.
* Ensure settings and configurations meet security requirements by having them reviewed by security specialists, tools designed for this purpose, or both.
* You need to prepare now for post quantum cryptography (PQC), see reference (ENISA) so that high risk systems are safe no later than the end of 2030.


## Example attack scenarios. 

**Scenario #1**: A site doesn't use or enforce TLS for all pages or supports weak encryption. An attacker monitors network traffic (e.g., at an insecure wireless network), downgrades connections from HTTPS to HTTP, intercepts requests, and steals the user's session cookie. The attacker then replays this cookie and hijacks the user's (authenticated) session, accessing or modifying the user's private data. Instead of the above they could alter all transported data, e.g., the recipient of a money transfer.

**Scenario #2**: The password database uses unsalted or simple hashes to store everyone's passwords. A file upload flaw allows an attacker to retrieve the password database. All the unsalted hashes can be exposed with a rainbow table of pre-calculated hashes. Hashes generated by simple or fast hash functions may be cracked by GPUs, even if they were salted.


## References.



* [OWASP Proactive Controls: C2: Use Cryptography to Protect Data ](https://top10proactive.owasp.org/archive/2024/the-top-10/c2-crypto/)
* [OWASP Application Security Verification Standard (ASVS): ](https://owasp.org/www-project-application-security-verification-standard) [V11,](https://github.com/OWASP/ASVS/blob/v5.0.0/5.0/en/0x20-V11-Cryptography.md) [12, ](https://github.com/OWASP/ASVS/blob/v5.0.0/5.0/en/0x21-V12-Secure-Communication.md) [14](https://github.com/OWASP/ASVS/blob/v5.0.0/5.0/en/0x23-V14-Data-Protection.md)
* [OWASP Cheat Sheet: Transport Layer Protection](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)
* [OWASP Cheat Sheet: User Privacy Protection](https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html)
* [OWASP Cheat Sheet: Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
* [OWASP Cheat Sheet: Cryptographic Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
* [OWASP Cheat Sheet: HSTS](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html)
* [OWASP Testing Guide: Testing for weak cryptography](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/README)
* [ENISA: A Coordinated Implementation Roadmap for the Transition to Post-Quantum Cryptography](https://digital-strategy.ec.europa.eu/en/library/coordinated-implementation-roadmap-transition-post-quantum-cryptography)
* [NIST Releases First 3 Finalized Post-Quantum Encryption Standards](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)


## List of Mapped CWEs

* [CWE-261 Weak Encoding for Password](https://cwe.mitre.org/data/definitions/261.html)

* [CWE-296 Improper Following of a Certificate's Chain of Trust](https://cwe.mitre.org/data/definitions/296.html)

* [CWE-319 Cleartext Transmission of Sensitive Information](https://cwe.mitre.org/data/definitions/319.html)

* [CWE-320 Key Management Errors (Prohibited)](https://cwe.mitre.org/data/definitions/320.html)

* [CWE-321 Use of Hard-coded Cryptographic Key](https://cwe.mitre.org/data/definitions/321.html)

* [CWE-322 Key Exchange without Entity Authentication](https://cwe.mitre.org/data/definitions/322.html)

* [CWE-323 Reusing a Nonce, Key Pair in Encryption](https://cwe.mitre.org/data/definitions/323.html)

* [CWE-324 Use of a Key Past its Expiration Date](https://cwe.mitre.org/data/definitions/324.html)

* [CWE-325 Missing Required Cryptographic Step](https://cwe.mitre.org/data/definitions/325.html)

* [CWE-326 Inadequate Encryption Strength](https://cwe.mitre.org/data/definitions/326.html)

* [CWE-327 Use of a Broken or Risky Cryptographic Algorithm](https://cwe.mitre.org/data/definitions/327.html)

* [CWE-328 Reversible One-Way Hash](https://cwe.mitre.org/data/definitions/328.html)

* [CWE-329 Not Using a Random IV with CBC Mode](https://cwe.mitre.org/data/definitions/329.html)

* [CWE-330 Use of Insufficiently Random Values](https://cwe.mitre.org/data/definitions/330.html)

* [CWE-331 Insufficient Entropy](https://cwe.mitre.org/data/definitions/331.html)

* [CWE-332 Insufficient Entropy in PRNG](https://cwe.mitre.org/data/definitions/332.html)

* [CWE-334 Small Space of Random Values](https://cwe.mitre.org/data/definitions/334.html)

* [CWE-335 Incorrect Usage of Seeds in Pseudo-Random Number Generator(PRNG)](https://cwe.mitre.org/data/definitions/335.html)

* [CWE-336 Same Seed in Pseudo-Random Number Generator (PRNG)](https://cwe.mitre.org/data/definitions/336.html)

* [CWE-337 Predictable Seed in Pseudo-Random Number Generator (PRNG)](https://cwe.mitre.org/data/definitions/337.html)

* [CWE-338 Use of Cryptographically Weak Pseudo-Random Number Generator(PRNG)](https://cwe.mitre.org/data/definitions/338.html)

* [CWE-340 Generation of Predictable Numbers or Identifiers](https://cwe.mitre.org/data/definitions/340.html)

* [CWE-342 Predictable Exact Value from Previous Values](https://cwe.mitre.org/data/definitions/342.html)

* [CWE-347 Improper Verification of Cryptographic Signature](https://cwe.mitre.org/data/definitions/347.html)

* [CWE-523 Unprotected Transport of Credentials](https://cwe.mitre.org/data/definitions/523.html)

* [CWE-757 Selection of Less-Secure Algorithm During Negotiation('Algorithm Downgrade')](https://cwe.mitre.org/data/definitions/757.html)

* [CWE-759 Use of a One-Way Hash without a Salt](https://cwe.mitre.org/data/definitions/759.html)

* [CWE-760 Use of a One-Way Hash with a Predictable Salt](https://cwe.mitre.org/data/definitions/760.html)

* [CWE-780 Use of RSA Algorithm without OAEP](https://cwe.mitre.org/data/definitions/780.html)

* [CWE-916 Use of Password Hash With Insufficient Computational Effort](https://cwe.mitre.org/data/definitions/916.html)

* [CWE-1240 Use of a Cryptographic Primitive with a Risky Implementation](https://cwe.mitre.org/data/definitions/1240.html)

* [CWE-1241 Use of Predictable Algorithm in Random Number Generator](https://cwe.mitre.org/data/definitions/1241.html)

---

## Section 6: A05 2025-Injection

# A05:2025 Injection ![icon](../assets/TOP_10_Icons_Final_Injection.png){: style="height:80px;width:80px" align="right"}

## Background. 

Injection falls two spots from #3 to #5 in the ranking, maintaining its position relative to A04:2025-Cryptographic Failures and A06:2025-Insecure Design. Injection is one of the most tested categories with 100% of applications tested for some form of injection. It had the greatest number of CVEs for any category, with 37 CWEs in this category. Injection includes Cross-site Scripting (high frequency/low impact) with more than 30k CVEs and SQL Injection (low frequency/high impact) with more than 14k CVEs. The massive number of reported CVEs for CWE-79 Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') brings down the average weighted impact of this category. 


## Score table.


<table>
  <tr>
   <td>CWEs Mapped 
   </td>
   <td>Max Incidence Rate
   </td>
   <td>Avg Incidence Rate
   </td>
   <td>Max Coverage
   </td>
   <td>Avg Coverage
   </td>
   <td>Avg Weighted Exploit
   </td>
   <td>Avg Weighted Impact
   </td>
   <td>Total Occurrences
   </td>
   <td>Total CVEs
   </td>
  </tr>
  <tr>
   <td>37
   </td>
   <td>13.77%
   </td>
   <td>3.08%
   </td>
   <td>100.00%
   </td>
   <td>42.93%
   </td>
   <td>7.15
   </td>
   <td>4.32
   </td>
   <td>1,404,249
   </td>
   <td>62,445
   </td>
  </tr>
</table>



## Description. 

An injection vulnerability is an application flaw that allows untrusted user input to be sent to an interpreter (e.g. a browser, database, the command line) and causes the interpreter to execute parts of that input as commands. 

An application is vulnerable to attack when:

* User-supplied data is not validated, filtered, or sanitized by the application.
* Dynamic queries or non-parameterized calls without context-aware escaping are used directly in the interpreter.
* Unsanitized data is used within object-relational mapping (ORM) search parameters to extract additional, sensitive records.
* Potentially hostile data is directly used or concatenated. The SQL or command contains the structure and malicious data in dynamic queries, commands, or stored procedures.

Some of the more common injections are SQL, NoSQL, OS command, Object Relational Mapping (ORM), LDAP, and Expression Language (EL) or Object Graph Navigation Library (OGNL) injection. The concept is identical among all interpreters. Detection is best achieved by a combination of source code review along with automated testing (including fuzzing) of all parameters, headers, URL, cookies, JSON, SOAP, and XML data inputs. The addition of static (SAST), dynamic (DAST), and interactive (IAST) application security testing tools into the CI/CD pipeline can also be helpful to identify injection flaws before production deployment.

A related class of injection vulnerabilities has become common in LLMs. These are discussed separately in the [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/), specifically [LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/).


## How to prevent. 

The best means to prevent injection requires keeping data separate from commands and queries:

* The preferred option is to use a safe API, which avoids using the interpreter entirely, provides a parameterized interface, or migrates to Object Relational Mapping Tools (ORMs). 
**Note:** Even when parameterized, stored procedures can still introduce SQL injection if PL/SQL or T-SQL concatenates queries and data or executes hostile data with EXECUTE IMMEDIATE or exec().

When it is not possible to separate the data from commands, you can reduce threats using the following techniques. 

* Use positive server-side input validation. This is not a complete defense as many applications require special characters, such as text areas or APIs for mobile applications.
* For any residual dynamic queries, escape special characters using the specific escape syntax for that interpreter. 
**Note:** SQL structures such as table names, column names, and so on cannot be escaped, and thus user-supplied structure names are dangerous. This is a common issue in report-writing software.

**Warning** these techniques involve parsing and escaping complex strings, making them error-prone and not robust in the face of minor changes to the underlying system. 

## Example attack scenarios.

**Scenario #1:** An application uses untrusted data in the construction of the following vulnerable SQL call:

```
String query = "SELECT * FROM accounts WHERE custID='" + request.getParameter("id") + "'";
```

An attacker modifies the 'id' parameter value in their browser to send: `' OR '1'='1`. For example:

```
http://example.com/app/accountView?id=' OR '1'='1
```

This changes the meaning of the query to return all records from the accounts table. More dangerous attacks could modify or delete data or even invoke stored procedures.

**Scenario #2:** An application's blind trust in frameworks may result in queries that are still vulnerable. For example, Hibernate Query Language (HQL):

```
Query HQLQuery = session.createQuery("FROM accounts WHERE custID='" + request.getParameter("id") + "'");
```

An attacker supplies: `' OR custID IS NOT NULL OR custID='`. This bypasses the filter and returns all accounts. While HQL has fewer dangerous functions than raw SQL, it still allows unauthorized data access when user input is concatenated into queries.

**Scenario #3:** An application passes user input directly to an OS command:

```
String cmd = "nslookup " + request.getParameter("domain");
Runtime.getRuntime().exec(cmd);
```

An attacker supplies `example.com; cat /etc/passwd` to execute arbitrary commands on the server.

## References.

* [OWASP Proactive Controls: Secure Database Access](https://owasp.org/www-project-proactive-controls/v3/en/c3-secure-database)
* [OWASP ASVS: V5 Input Validation and Encoding](https://owasp.org/www-project-application-security-verification-standard)
* [OWASP Testing Guide: SQL Injection,](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection) [Command Injection](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/12-Testing_for_Command_Injection), and [ORM Injection](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05.7-Testing_for_ORM_Injection)
* [OWASP Cheat Sheet: Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html)
* [OWASP Cheat Sheet: SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
* [OWASP Cheat Sheet: Injection Prevention in Java](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet_in_Java.html)
* [OWASP Cheat Sheet: Query Parameterization](https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html)
* [OWASP Automated Threats to Web Applications – OAT-014](https://owasp.org/www-project-automated-threats-to-web-applications/)
* [PortSwigger: Server-side template injection](https://portswigger.net/kb/issues/00101080_serversidetemplateinjection)
* [Awesome Fuzzing: a list of fuzzing resources](https://github.com/secfigo/Awesome-Fuzzing) 



## List of Mapped CWEs

* [CWE-20 Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)

* [CWE-74 Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection')](https://cwe.mitre.org/data/definitions/74.html)

* [CWE-76 Improper Neutralization of Equivalent Special Elements](https://cwe.mitre.org/data/definitions/76.html)

* [CWE-77 Improper Neutralization of Special Elements used in a Command ('Command Injection')](https://cwe.mitre.org/data/definitions/77.html)

* [CWE-78 Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')](https://cwe.mitre.org/data/definitions/78.html)

* [CWE-79 Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')](https://cwe.mitre.org/data/definitions/79.html)

* [CWE-80 Improper Neutralization of Script-Related HTML Tags in a Web Page (Basic XSS)](https://cwe.mitre.org/data/definitions/80.html)

* [CWE-83 Improper Neutralization of Script in Attributes in a Web Page](https://cwe.mitre.org/data/definitions/83.html)

* [CWE-86 Improper Neutralization of Invalid Characters in Identifiers in Web Pages](https://cwe.mitre.org/data/definitions/86.html)

* [CWE-88 Improper Neutralization of Argument Delimiters in a Command ('Argument Injection')](https://cwe.mitre.org/data/definitions/88.html)

* [CWE-89 Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')](https://cwe.mitre.org/data/definitions/89.html)

* [CWE-90 Improper Neutralization of Special Elements used in an LDAP Query ('LDAP Injection')](https://cwe.mitre.org/data/definitions/90.html)

* [CWE-91 XML Injection (aka Blind XPath Injection)](https://cwe.mitre.org/data/definitions/91.html)

* [CWE-93 Improper Neutralization of CRLF Sequences ('CRLF Injection')](https://cwe.mitre.org/data/definitions/93.html)

* [CWE-94 Improper Control of Generation of Code ('Code Injection')](https://cwe.mitre.org/data/definitions/94.html)

* [CWE-95 Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection')](https://cwe.mitre.org/data/definitions/95.html)

* [CWE-96 Improper Neutralization of Directives in Statically Saved Code ('Static Code Injection')](https://cwe.mitre.org/data/definitions/96.html)

* [CWE-97 Improper Neutralization of Server-Side Includes (SSI) Within a Web Page](https://cwe.mitre.org/data/definitions/97.html)

* [CWE-98 Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion')](https://cwe.mitre.org/data/definitions/98.html)

* [CWE-99 Improper Control of Resource Identifiers ('Resource Injection')](https://cwe.mitre.org/data/definitions/99.html)

* [CWE-103 Struts: Incomplete validate() Method Definition](https://cwe.mitre.org/data/definitions/103.html)

* [CWE-104 Struts: Form Bean Does Not Extend Validation Class](https://cwe.mitre.org/data/definitions/104.html)

* [CWE-112 Missing XML Validation](https://cwe.mitre.org/data/definitions/112.html)

* [CWE-113 Improper Neutralization of CRLF Sequences in HTTP Headers ('HTTP Response Splitting')](https://cwe.mitre.org/data/definitions/113.html)

* [CWE-114 Process Control](https://cwe.mitre.org/data/definitions/114.html)

* [CWE-115 Misinterpretation of Output](https://cwe.mitre.org/data/definitions/115.html)

* [CWE-116 Improper Encoding or Escaping of Output](https://cwe.mitre.org/data/definitions/116.html)

* [CWE-129 Improper Validation of Array Index](https://cwe.mitre.org/data/definitions/129.html)

* [CWE-159 Improper Handling of Invalid Use of Special Elements](https://cwe.mitre.org/data/definitions/159.html)

* [CWE-470 Use of Externally-Controlled Input to Select Classes or Code ('Unsafe Reflection')](https://cwe.mitre.org/data/definitions/470.html)

* [CWE-493 Critical Public Variable Without Final Modifier](https://cwe.mitre.org/data/definitions/493.html)

* [CWE-500 Public Static Field Not Marked Final](https://cwe.mitre.org/data/definitions/500.html)

* [CWE-564 SQL Injection: Hibernate](https://cwe.mitre.org/data/definitions/564.html)

* [CWE-610 Externally Controlled Reference to a Resource in Another Sphere](https://cwe.mitre.org/data/definitions/610.html)

* [CWE-643 Improper Neutralization of Data within XPath Expressions ('XPath Injection')](https://cwe.mitre.org/data/definitions/643.html)

* [CWE-644 Improper Neutralization of HTTP Headers for Scripting Syntax](https://cwe.mitre.org/data/definitions/644.html)

* [CWE-917 Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection')](https://cwe.mitre.org/data/definitions/917.html)

---

## Section 7: A06 2025-Insecure Design

# A06:2025 Insecure Design ![icon](../assets/TOP_10_Icons_Final_Insecure_Design.png){: style="height:80px;width:80px" align="right"}


## Background. 

Insecure Design slides two spots from #4 to #6 in the ranking as **[A02:2025-Security Misconfiguration](A02_2025-Security_Misconfiguration.md)** and **[A03:2025-Software Supply Chain Failures](A03_2025-Software_Supply_Chain_Failures.md)** leapfrog it. This category was introduced in 2021, and we have seen noticeable improvements in the industry related to threat modeling and a greater emphasis on secure design. This category focuses on risks related to design and architectural flaws, with a call for more use of threat modeling, secure design patterns, and reference architectures. This includes flaws in the business logic of an application, e.g. the lack of defining unwanted or unexpected state changes inside an application.  As a community, we need to move beyond "shift-left" in the coding space, to pre-code activities such as requirements writing and application design, that are critical for the principles of Secure by Design (e.g. see **[Establish a Modern AppSec Program: Planning and Design Phase](0x03_2025-Establishing_a_Modern_Application_Security_Program.md)**). Notable Common Weakness Enumerations (CWEs) include *CWE-256: Unprotected Storage of Credentials, CWE-269 Improper Privilege Management, CWE-434 Unrestricted Upload of File with Dangerous Type, CWE-501: Trust Boundary Violation, and CWE-522: Insufficiently Protected Credentials.*


## Score table.


<table>
  <tr>
   <td>CWEs Mapped 
   </td>
   <td>Max Incidence Rate
   </td>
   <td>Avg Incidence Rate
   </td>
   <td>Max Coverage
   </td>
   <td>Avg Coverage
   </td>
   <td>Avg Weighted Exploit
   </td>
   <td>Avg Weighted Impact
   </td>
   <td>Total Occurrences
   </td>
   <td>Total CVEs
   </td>
  </tr>
  <tr>
   <td>39
   </td>
   <td>22.18%
   </td>
   <td>1.86%
   </td>
   <td>88.76%
   </td>
   <td>35.18%
   </td>
   <td>6.96
   </td>
   <td>4.05
   </td>
   <td>729,882
   </td>
   <td>7,647
   </td>
  </tr>
</table>



## Description. 

Insecure design is a broad category representing different weaknesses, expressed as “missing or ineffective control design.” Insecure design is not the source for all other Top Ten risk categories. Note that there is a difference between insecure design and insecure implementation. We differentiate between design flaws and implementation defects for a reason, they have different root causes, take place at different times in the development process, and have different remediations. A secure design can still have implementation defects leading to vulnerabilities that may be exploited. An insecure design cannot be fixed by a perfect implementation as needed security controls were never created to defend against specific attacks. One of the factors that contributes to insecure design is the lack of business risk profiling inherent in the software or system being developed, and thus the failure to determine what level of security design is required.

Three key parts of having a secure design are:

* Gathering Requirements and Resource Management
* Creating a Secure Design
* Having a Secure Development Lifecycle


### Requirements and Resource Management

Collect and negotiate the business requirements for an application with the business, including the protection requirements concerning confidentiality, integrity, availability, and authenticity of all data assets and the expected business logic. Take into account how exposed your application will be and if you need segregation of tenants (beyond those needed for access control). Compile the technical requirements, including functional and non-functional security requirements. Plan and negotiate the budget covering all design, build, testing, and operation, including security activities.


### Secure Design

Secure design is a culture and methodology that constantly evaluates threats and ensures that code is robustly designed and tested to prevent known attack methods. Threat modeling should be integrated into refinement sessions (or similar activities); look for changes in data flows and access control or other security controls. In the  story development, determine the correct flow and failure states, ensure they are well understood and agreed upon by the responsible and impacted parties. Analyze assumptions and conditions for expected and failure flows to ensure they remain accurate and desirable. Determine how to validate the assumptions and enforce conditions needed for proper behaviors. Ensure the results are documented in the  story. Learn from mistakes and offer positive incentives to promote improvements. Secure design is neither an add-on nor a tool that you can add to software.


### Secure Development Lifecycle

Secure software requires a secure development lifecycle, a secure design pattern, a paved road methodology, a secure component library, appropriate tooling, threat modeling, and incident post-mortems that are used to improve the process. Reach out to your security specialists at the beginning of a software project, throughout the project, and for ongoing software maintenance. Consider leveraging the [OWASP Software Assurance Maturity Model (SAMM)](https://owaspsamm.org/) to help structure your secure software development efforts.

Often self-responsibility of developers is underappreciated. Foster a culture of awareness, responsibility and proactive risk mitigation. Regular exchanges about security (e.g. during threat modeling sessions) can generate a mindset for including security in all important design decisions.  


## How to prevent. 



* Establish and use a secure development lifecycle with AppSec professionals to help evaluate and design security and privacy-related controls
* Establish and use a library of secure design patterns or paved-road components
* Use threat modeling for critical parts of the application such as authentication, access control, business logic, and key flows
* Use threat modeling as an educational tool to generate a security mindset
* Integrate security language and controls into user stories
* Integrate plausibility checks at each tier of your application (from frontend to backend)
* Write unit and integration tests to validate that all critical flows are resistant to the threat model. Compile use-cases *and* misuse-cases for each tier of your application.
* Segregate tier layers on the system and network layers, depending on the exposure and protection needs
* Segregate tenants robustly by design throughout all tiers


## Example attack scenarios. 

**Scenario #1:** A credential recovery workflow might include “questions and answers,” which is prohibited by NIST 800-63b, the OWASP ASVS, and the OWASP Top 10. Questions and answers cannot be trusted as evidence of identity, as more than one person can know the answers. Such functionality should be removed and replaced with a more secure design.

**Scenario #2:** A cinema chain allows group booking discounts and has a maximum of fifteen attendees before requiring a deposit. Attackers could threat model this flow and test if they can find an attack vector in the business logic of the application, e.g. booking six hundred seats and all cinemas at once in a few requests, causing a massive loss of income.

**Scenario #3:** A retail chain’s e-commerce website does not have protection against bots run by scalpers buying high-end video cards to resell on auction websites. This creates terrible publicity for the video card makers and retail chain owners, and enduring bad blood with enthusiasts who cannot obtain these cards at any price. Careful anti-bot design and domain logic rules, such as purchases made within a few seconds of availability, might identify inauthentic purchases and reject such transactions.


## References.



* [OWASP Cheat Sheet: Secure Design Principles](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Product_Design_Cheat_Sheet.html)
* [OWASP SAMM: Design | Secure Architecture](https://owaspsamm.org/model/design/secure-architecture/)
* [OWASP SAMM: Design | Threat Assessment](https://owaspsamm.org/model/design/threat-assessment/)
* [NIST – Guidelines on Minimum Standards for Developer Verification of Software](https://www.nist.gov/publications/guidelines-minimum-standards-developer-verification-software)
* [The Threat Modeling Manifesto](https://threatmodelingmanifesto.org/)
* [Awesome Threat Modeling](https://github.com/hysnsec/awesome-threat-modelling)


## List of Mapped CWEs

* [CWE-73 External Control of File Name or Path](https://cwe.mitre.org/data/definitions/73.html)

* [CWE-183 Permissive List of Allowed Inputs](https://cwe.mitre.org/data/definitions/183.html)

* [CWE-256 Unprotected Storage of Credentials](https://cwe.mitre.org/data/definitions/256.html)

* [CWE-266 Incorrect Privilege Assignment](https://cwe.mitre.org/data/definitions/266.html)

* [CWE-269 Improper Privilege Management](https://cwe.mitre.org/data/definitions/269.html)

* [CWE-286 Incorrect User Management](https://cwe.mitre.org/data/definitions/286.html)

* [CWE-311 Missing Encryption of Sensitive Data](https://cwe.mitre.org/data/definitions/311.html)

* [CWE-312 Cleartext Storage of Sensitive Information](https://cwe.mitre.org/data/definitions/312.html)

* [CWE-313 Cleartext Storage in a File or on Disk](https://cwe.mitre.org/data/definitions/313.html)

* [CWE-316 Cleartext Storage of Sensitive Information in Memory](https://cwe.mitre.org/data/definitions/316.html)

* [CWE-362 Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition')](https://cwe.mitre.org/data/definitions/362.html)

* [CWE-382 J2EE Bad Practices: Use of System.exit()](https://cwe.mitre.org/data/definitions/382.html)

* [CWE-419 Unprotected Primary Channel](https://cwe.mitre.org/data/definitions/419.html)

* [CWE-434 Unrestricted Upload of File with Dangerous Type](https://cwe.mitre.org/data/definitions/434.html)

* [CWE-436 Interpretation Conflict](https://cwe.mitre.org/data/definitions/436.html)

* [CWE-444 Inconsistent Interpretation of HTTP Requests ('HTTP Request Smuggling')](https://cwe.mitre.org/data/definitions/444.html)

* [CWE-451 User Interface (UI) Misrepresentation of Critical Information](https://cwe.mitre.org/data/definitions/451.html)

* [CWE-454 External Initialization of Trusted Variables or Data Stores](https://cwe.mitre.org/data/definitions/454.html)

* [CWE-472 External Control of Assumed-Immutable Web Parameter](https://cwe.mitre.org/data/definitions/472.html)

* [CWE-501 Trust Boundary Violation](https://cwe.mitre.org/data/definitions/501.html)

* [CWE-522 Insufficiently Protected Credentials](https://cwe.mitre.org/data/definitions/522.html)

* [CWE-525 Use of Web Browser Cache Containing Sensitive Information](https://cwe.mitre.org/data/definitions/525.html)

* [CWE-539 Use of Persistent Cookies Containing Sensitive Information](https://cwe.mitre.org/data/definitions/539.html)

* [CWE-598 Use of GET Request Method With Sensitive Query Strings](https://cwe.mitre.org/data/definitions/598.html)

* [CWE-602 Client-Side Enforcement of Server-Side Security](https://cwe.mitre.org/data/definitions/602.html)

* [CWE-628 Function Call with Incorrectly Specified Arguments](https://cwe.mitre.org/data/definitions/628.html)

* [CWE-642 External Control of Critical State Data](https://cwe.mitre.org/data/definitions/642.html)

* [CWE-646 Reliance on File Name or Extension of Externally-Supplied File](https://cwe.mitre.org/data/definitions/646.html)

* [CWE-653 Insufficient Compartmentalization](https://cwe.mitre.org/data/definitions/653.html)

* [CWE-656 Reliance on Security Through Obscurity](https://cwe.mitre.org/data/definitions/656.html)

* [CWE-657 Violation of Secure Design Principles](https://cwe.mitre.org/data/definitions/657.html)

* [CWE-676 Use of Potentially Dangerous Function](https://cwe.mitre.org/data/definitions/676.html)

* [CWE-693 Protection Mechanism Failure](https://cwe.mitre.org/data/definitions/693.html)

* [CWE-799 Improper Control of Interaction Frequency](https://cwe.mitre.org/data/definitions/799.html)

* [CWE-807 Reliance on Untrusted Inputs in a Security Decision](https://cwe.mitre.org/data/definitions/807.html)

* [CWE-841 Improper Enforcement of Behavioral Workflow](https://cwe.mitre.org/data/definitions/841.html)

* [CWE-1021 Improper Restriction of Rendered UI Layers or Frames](https://cwe.mitre.org/data/definitions/1021.html)

* [CWE-1022 Use of Web Link to Untrusted Target with window.opener Access](https://cwe.mitre.org/data/definitions/1022.html)

* [CWE-1125 Excessive Attack Surface](https://cwe.mitre.org/data/definitions/1125.html)

---

## Section 8: A07 2025-Authentication Failures

# A07:2025 Authentication Failures ![icon](../assets/TOP_10_Icons_Final_Identification_and_Authentication_Failures.png){: style="height:80px;width:80px" align="right"}


## Background. 

Authentication Failures maintains its position at #7 with a slight name change to more accurately reflect the 36 CWEs in this category. Despite benefits from standardized frameworks, this category has kept its #7 rank from 2021. Notable CWEs included are *CWE-259 Use of Hard-coded Password*, *CWE-297: Improper Validation of Certificate with Host Mismatch*, *CWE-287: Improper Authentication*, *CWE-384: Session Fixation*, and *CWE-798 Use of Hard-coded Credentials*.


## Score table.


<table>
  <tr>
   <td>CWEs Mapped 
   </td>
   <td>Max Incidence Rate
   </td>
   <td>Avg Incidence Rate
   </td>
   <td>Max Coverage
   </td>
   <td>Avg Coverage
   </td>
   <td>Avg Weighted Exploit
   </td>
   <td>Avg Weighted Impact
   </td>
   <td>Total Occurrences
   </td>
   <td>Total CVEs
   </td>
  </tr>
  <tr>
   <td>36
   </td>
   <td>15.80%
   </td>
   <td>2.92%
   </td>
   <td>100.00%
   </td>
   <td>37.14%
   </td>
   <td>7.69
   </td>
   <td>4.44
   </td>
   <td>1,120,673
   </td>
   <td>7,147
   </td>
  </tr>
</table>



## Description. 

When an attacker is able to trick a system into recognizing an invalid or incorrect user as legitimate, this vulnerability is present. There may be authentication weaknesses if the application:

* Permits automated attacks such as credential stuffing, where the attacker has a breached list of valid usernames and passwords. More recently this type of attack has been expanded to include hybrid password attacks credential stuffing (also known as password spray attacks), where the attacker uses variations or increments of spilled credentials to gain access, for instance trying Password1!, Password2!, Password3! and so on.

* Permits brute force or other automated, scripted attacks that are not quickly blocked.

* Permits default, weak, or well-known passwords, such as "Password1" or "admin" username with an "admin" password.

* Allows users to create new accounts with already known-breached credentials.

* Allows use of weak or ineffective credential recovery and forgot-password processes, such as "knowledge-based answers," which cannot be made safe.

* Uses plain text, encrypted, or weakly hashed passwords data stores (see[ A04:2025-Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/)).

* Has missing or ineffective multi-factor authentication.

* Allows use of weak or ineffective fallbacks if multi-factor authentication is not available. 

* Exposes session identifier in the URL, a hidden field, or another insecure location that is accessible to the client.

* Reuses the same session identifier after successful login.

* Does not correctly invalidate user sessions or authentication tokens (mainly single sign-on (SSO) tokens) during logout or a period of inactivity.

* Does not correctly assert the scope and intended audience of the provided credentials.

## How to prevent. 

* Where possible, implement and enforce use of multi-factor authentication to prevent automated credential stuffing, brute force, and stolen credential reuse attacks.

* Where possible, encourage and enable the use of password managers, to help users make better choices.

* Do not ship or deploy with any default credentials, particularly for admin users.

* Implement weak password checks, such as testing new or changed passwords against the top 10,000 worst passwords list.

* During new account creation and password changes validate against lists of known breached credentials (eg: using [haveibeenpwned.com](https://haveibeenpwned.com)).

* Align password length, complexity, and rotation policies with [National Institute of Standards and Technology (NIST) 800-63b's guidelines in section 5.1.1](https://pages.nist.gov/800-63-3/sp800-63b.html#:~:text=5.1.1%20Memorized%20Secrets) for Memorized Secrets or other modern, evidence-based password policies.

* Do not force human beings to rotate passwords unless you suspect breach. If you suspect breach, force password resets immediately. 

* Ensure registration, credential recovery, and API pathways are hardened against account enumeration attacks by using the same messages for all outcomes (“Invalid username or password.”).

* Limit or increasingly delay failed login attempts but be careful not to create a denial of service scenario. Log all failures and alert administrators when credential stuffing, brute force, or other attacks are detected or suspected.

* Use a server-side, secure, built-in session manager that generates a new random session ID with high entropy after login. Session identifiers should not be in the URL, be securely stored in a secure cookie, and invalidated after logout, idle, and absolute timeouts. 

* Ideally, use a premade, well-trusted system to handle authentication, identity, and session management. Transfer this risk whenever possible by buying and utilizing a hardened and well tested system.

* Verify the intended use of provided credentials, e.g. for JWTs validate `aud`, `iss` claims and scopes


## Example attack scenarios. 

**Scenario #1:** Credential stuffing, the use of lists of known username and password combinations, is now a very common attack. More recently attackers have been found to ‘increment’ or otherwise adjust passwords, based on common human behavior. For instance, changing ‘Winter2025’ to ‘Winter2026’, or ‘ILoveMyDog6’ to ‘ILoveMyDog7’ or ‘ILoveMyDog5’. This adjusting of password attempts is called a hybrid credential stuffing attack or a password spray attack, and they can be even more effective than the traditional version. If an application does not implement defences against automated threats (brute force, scripts, or bots) or credential stuffing, the application can be used as a password oracle to determine if the credentials are valid and gain unauthorized access.

**Scenario #2:** Most successful authentication attacks occur due to the continued use of passwords as the sole authentication factor. Once considered best practices, password rotation and complexity requirements encourage users to both reuse passwords and use weak passwords. Organizations are recommended to stop these practices per NIST 800-63 and to enforce use of multi-factor authentication on all important systems.

**Scenario #3:** Application session timeouts aren't implemented correctly. A user uses a public computer to access an application and instead of selecting "logout," the user simply closes the browser tab and walks away. Another Example for this is, if a Single Sign on (SSO) session can not be closed by a Single Logout (SLO). That is, a single login logs you into, for example, your mail reader, your document system, and your chat system. But logging out happens only to the current system. If an attacker uses the same browser after the victim thinks they have successfully logged out, but with the user still authenticated to some of the applications, then can access the victim's account. The same issue can happen in offices and enterprises when a sensitive application has not been properly exited and a colleague has (temporary) access to the unlocked computer.

## References.

* [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

* [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/stable-en/01-introduction/05-introduction)


## List of Mapped CWEs

* [CWE-258 Empty Password in Configuration File](https://cwe.mitre.org/data/definitions/258.html)

* [CWE-259 Use of Hard-coded Password](https://cwe.mitre.org/data/definitions/259.html)

* [CWE-287 Improper Authentication](https://cwe.mitre.org/data/definitions/287.html)

* [CWE-288 Authentication Bypass Using an Alternate Path or Channel](https://cwe.mitre.org/data/definitions/288.html)

* [CWE-289 Authentication Bypass by Alternate Name](https://cwe.mitre.org/data/definitions/289.html)

* [CWE-290 Authentication Bypass by Spoofing](https://cwe.mitre.org/data/definitions/290.html)

* [CWE-291 Reliance on IP Address for Authentication](https://cwe.mitre.org/data/definitions/291.html)

* [CWE-293 Using Referer Field for Authentication](https://cwe.mitre.org/data/definitions/293.html)

* [CWE-294 Authentication Bypass by Capture-replay](https://cwe.mitre.org/data/definitions/294.html)

* [CWE-295 Improper Certificate Validation](https://cwe.mitre.org/data/definitions/295.html)

* [CWE-297 Improper Validation of Certificate with Host Mismatch](https://cwe.mitre.org/data/definitions/297.html)

* [CWE-298 Improper Validation of Certificate with Host Mismatch](https://cwe.mitre.org/data/definitions/298.html)

* [CWE-299 Improper Validation of Certificate with Host Mismatch](https://cwe.mitre.org/data/definitions/299.html)

* [CWE-300 Channel Accessible by Non-Endpoint](https://cwe.mitre.org/data/definitions/300.html)

* [CWE-302 Authentication Bypass by Assumed-Immutable Data](https://cwe.mitre.org/data/definitions/302.html)

* [CWE-303 Incorrect Implementation of Authentication Algorithm](https://cwe.mitre.org/data/definitions/303.html)

* [CWE-304 Missing Critical Step in Authentication](https://cwe.mitre.org/data/definitions/304.html)

* [CWE-305 Authentication Bypass by Primary Weakness](https://cwe.mitre.org/data/definitions/305.html)

* [CWE-306 Missing Authentication for Critical Function](https://cwe.mitre.org/data/definitions/306.html)

* [CWE-307 Improper Restriction of Excessive Authentication Attempts](https://cwe.mitre.org/data/definitions/307.html)

* [CWE-308 Use of Single-factor Authentication](https://cwe.mitre.org/data/definitions/308.html)

* [CWE-309 Use of Password System for Primary Authentication](https://cwe.mitre.org/data/definitions/309.html)

* [CWE-346 Origin Validation Error](https://cwe.mitre.org/data/definitions/346.html)

* [CWE-350 Reliance on Reverse DNS Resolution for a Security-Critical Action](https://cwe.mitre.org/data/definitions/350.html)

* [CWE-384 Session Fixation](https://cwe.mitre.org/data/definitions/384.html)

* [CWE-521 Weak Password Requirements](https://cwe.mitre.org/data/definitions/521.html)

* [CWE-613 Insufficient Session Expiration](https://cwe.mitre.org/data/definitions/613.html)

* [CWE-620 Unverified Password Change](https://cwe.mitre.org/data/definitions/620.html)

* [CWE-640 Weak Password Recovery Mechanism for Forgotten Password](https://cwe.mitre.org/data/definitions/640.html)

* [CWE-798 Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)

* [CWE-940 Improper Verification of Source of a Communication Channel](https://cwe.mitre.org/data/definitions/940.html)

* [CWE-941 Incorrectly Specified Destination in a Communication Channel](https://cwe.mitre.org/data/definitions/941.html)

* [CWE-1390 Weak Authentication](https://cwe.mitre.org/data/definitions/1390.html)

* [CWE-1391 Use of Weak Credentials](https://cwe.mitre.org/data/definitions/1391.html)

* [CWE-1392 Use of Default Credentials](https://cwe.mitre.org/data/definitions/1392.html)

* [CWE-1393 Use of Default Password](https://cwe.mitre.org/data/definitions/1393.html)

---

## Section 9: A08 2025-Software Or Data Integrity Failures

# A08:2025 Software or Data Integrity Failures ![icon](../assets/TOP_10_Icons_Final_Software_and_Data_Integrity_Failures.png){: style="height:80px;width:80px" align="right"}

## Background. 

Software or Data Integrity Failures continues at #8, with a slight, clarifying name change from "Software *and* Data Integrity Failures". This category is focused on the failure to maintain trust boundaries and verify the integrity of software, code, and data artifacts at a lower level than Software Supply Chain Failures. This category focuses on making assumptions related to software updates and critical data, without verifying integrity. Notable Common Weakness Enumerations (CWEs) include *CWE-829: Inclusion of Functionality from Untrusted Control Sphere*, *CWE-915: Improperly Controlled Modification of Dynamically-Determined Object Attributes*, and *CWE-502: Deserialization of Untrusted Data*.


## Score table.


<table>
  <tr>
   <td>CWEs Mapped 
   </td>
   <td>Max Incidence Rate
   </td>
   <td>Avg Incidence Rate
   </td>
   <td>Max Coverage
   </td>
   <td>Avg Coverage
   </td>
   <td>Avg Weighted Exploit
   </td>
   <td>Avg Weighted Impact
   </td>
   <td>Total Occurrences
   </td>
   <td>Total CVEs
   </td>
  </tr>
  <tr>
   <td>14
   </td>
   <td>8.98%
   </td>
   <td>2.75%
   </td>
   <td>78.52%
   </td>
   <td>45.49%
   </td>
   <td>7.11
   </td>
   <td>4.79
   </td>
   <td>501,327
   </td>
   <td>3,331
   </td>
  </tr>
</table>



## Description. 

Software and data integrity failures relate to code and infrastructure that does not protect against invalid or untrusted code or data being treated as trusted and valid. An example of this is where an application relies upon plugins, libraries, or modules from untrusted sources, repositories, and content delivery networks (CDNs). An insecure CI/CD pipeline without consuming and providing software integrity checks can introduce the potential for unauthorized access, insecure or malicious code, or system compromise. Another example of this is a CI/CD that pulls code or artifacts from untrusted places and/or doesn’t verify them before use (by checking the signature or similar mechanism). Lastly, many applications now include auto-update functionality, where updates are downloaded without sufficient integrity verification and applied to the previously trusted application. Attackers could potentially upload their own updates to be distributed and run on all installations. Another example is where objects or data are encoded or serialized into a structure that an attacker can see and modify is vulnerable to insecure deserialization.


## How to prevent. 



* Use digital signatures or similar mechanisms to verify the software or data is from the expected source and has not been altered.
* Ensure libraries and dependencies, such as npm or Maven, are only consuming trusted repositories. If you have a higher risk profile, consider hosting an internal known-good repository that's vetted.
* Ensure that there is a review process for code and configuration changes to minimize the chance that malicious code or configuration could be introduced into your software pipeline.
* Ensure that your CI/CD pipeline has proper segregation, configuration, and access control to ensure the integrity of the code flowing through the build and deploy processes.
* Ensure that unsigned or unencrypted serialized data is not received from untrusted clients and subsequently used without some form of integrity check or digital signature to detect tampering or replay of the serialized data.


## Example attack scenarios. 

**Scenario #1 Inclusion of Web Functionality from an Untrusted Source:** A company uses an external service provider to provide support functionality. For convenience, it has a DNS mapping for `myCompany.SupportProvider.com` to `support.myCompany.com`. This means that all cookies, including authentication cookies, set on the `myCompany.com` domain will now be sent to the support provider. Anyone with access to the support provider’s infrastructure can steal the cookies of all of your users that have visited `support.myCompany.com` and perform a session hijacking attack.

**Scenario #2 Update without signing:** Many home routers, set-top boxes, device firmware, and others do not verify updates via signed firmware. Unsigned firmware is a growing target for attackers and is expected to only get worse. This is a major concern as many times there is no mechanism to remediate other than to fix in a future version and wait for previous versions to age out.

**Scenario #3 Use of Package from an Untrusted Source:** A developer has trouble finding the updated version of a package they are looking for, so they download it not from the regular, trusted package manager, but from a website online. The package is not signed, and thus there is no opportunity to ensure integrity. The package includes malicious code.

**Scenario #4 Insecure Deserialization:** A React application calls a set of Spring Boot microservices. Being functional programmers, they tried to ensure that their code is immutable. The solution they came up with is serializing the user state and passing it back and forth with each request. An attacker notices the "rO0" Java object signature (in base64) and uses the [Java Deserialization Scanner](https://github.com/federicodotta/Java-Deserialization-Scanner) to gain remote code execution on the application server.

## References.

* [OWASP Cheat Sheet: Software Supply Chain Security](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html)
* [OWASP Cheat Sheet: Infrastructure as Code](https://cheatsheetseries.owasp.org/cheatsheets/Infrastructure_as_Code_Security_Cheat_Sheet.html)
* [OWASP Cheat Sheet: Deserialization](https://wiki.owasp.org/index.php/Deserialization_Cheat_Sheet)
* [SAFECode Software Integrity Controls](https://safecode.org/publication/SAFECode_Software_Integrity_Controls0610.pdf)
* [A 'Worst Nightmare' Cyberattack: The Untold Story Of The SolarWinds Hack](https://www.npr.org/2021/04/16/985439655/a-worst-nightmare-cyberattack-the-untold-story-of-the-solarwinds-hack)
* [CodeCov Bash Uploader Compromise](https://about.codecov.io/security-update)
* [Securing DevOps by Julien Vehent](https://www.manning.com/books/securing-devops)
* [Insecure Deserialization by Tenendo](https://tenendo.com/insecure-deserialization/)


## List of Mapped CWEs

* [CWE-345 Insufficient Verification of Data Authenticity](https://cwe.mitre.org/data/definitions/345.html)

* [CWE-353 Missing Support for Integrity Check](https://cwe.mitre.org/data/definitions/353.html)

* [CWE-426 Untrusted Search Path](https://cwe.mitre.org/data/definitions/426.html)

* [CWE-427 Uncontrolled Search Path Element](https://cwe.mitre.org/data/definitions/427.html)

* [CWE-494 Download of Code Without Integrity Check](https://cwe.mitre.org/data/definitions/494.html)

* [CWE-502 Deserialization of Untrusted Data](https://cwe.mitre.org/data/definitions/502.html)

* [CWE-506 Embedded Malicious Code](https://cwe.mitre.org/data/definitions/506.html)

* [CWE-509 Replicating Malicious Code (Virus or Worm)](https://cwe.mitre.org/data/definitions/509.html)

* [CWE-565 Reliance on Cookies without Validation and Integrity Checking](https://cwe.mitre.org/data/definitions/565.html)

* [CWE-784 Reliance on Cookies without Validation and Integrity Checking in a Security Decision](https://cwe.mitre.org/data/definitions/784.html)

* [CWE-829 Inclusion of Functionality from Untrusted Control Sphere](https://cwe.mitre.org/data/definitions/829.html)

* [CWE-830 Inclusion of Web Functionality from an Untrusted Source](https://cwe.mitre.org/data/definitions/830.html)

* [CWE-915 Improperly Controlled Modification of Dynamically-Determined Object Attributes](https://cwe.mitre.org/data/definitions/915.html)

* [CWE-926 Improper Export of Android Application Components](https://cwe.mitre.org/data/definitions/926.html)

---

## Section 10: A09 2025-Security Logging And Alerting Failures

# A09:2025 Security Logging & Alerting Failures ![icon](../assets/TOP_10_Icons_Final_Security_Logging_and_Monitoring_Failures.png){: style="height:80px;width:80px" align="right"}


## Background. 

Security Logging & Alerting Failures retains its position at #9. This category has a slight name change to emphasize the alerting function needed to induce action on relevant logging events. This category will always be underrepresented in the data, and for the third time voted into a position in the list from the community survey participants. This category is incredibly difficult to test for, and has minimal representation in the CVE/CVSS data (only 723 CVEs); but can be very impactful for visibility and incident alerting and forensics. This category includes issues with *properly handling output encoding to log files (CWE-117), inserting sensitive data into log files (CWE-532), and insufficient logging (CWE-778).*


## Score table.


<table>
  <tr>
   <td>CWEs Mapped 
   </td>
   <td>Max Incidence Rate
   </td>
   <td>Avg Incidence Rate
   </td>
   <td>Max Coverage
   </td>
   <td>Avg Coverage
   </td>
   <td>Avg Weighted Exploit
   </td>
   <td>Avg Weighted Impact
   </td>
   <td>Total Occurrences
   </td>
   <td>Total CVEs
   </td>
  </tr>
  <tr>
   <td>5
   </td>
   <td>11.33%
   </td>
   <td>3.91%
   </td>
   <td>85.96%
   </td>
   <td>46.48%
   </td>
   <td>7.19
   </td>
   <td>2.65
   </td>
   <td>260,288
   </td>
   <td>723
   </td>
  </tr>
</table>



## Description. 

Without logging and monitoring, attacks and breaches cannot be detected, and without alerting it is very difficult to respond quickly and effectively during a security incident. Insufficient logging, continuous monitoring, detection, and alerting to initiate active responses occurs any time:


* Auditable events, such as logins, failed logins, and high-value transactions, are not logged or logged inconsistently (for instance, only logging successful logins, but not failed attempts).
* Warnings and errors generate no, inadequate, or unclear log messages.
* The integrity of logs is not properly protected from tampering.
* Logs of applications and APIs are not monitored for suspicious activity.
* Logs are only stored locally, and not properly backedup.
* Appropriate alerting thresholds and response escalation processes are not in place or effective. Alerts are not received or reviewed within a reasonable amount of time.
* Penetration testing and scans by dynamic application security testing (DAST) tools (such as Burp or ZAP) do not trigger alerts.
* The application cannot detect, escalate, or alert for active attacks in real-time or near real-time.
* You are vulnerable to sensitive information leakage by making logging and alerting events visible to a user or an attacker (see [A01:2025-Broken Access Control](A01_2025-Broken_Access_Control.md)), or by logging sensitive information that should not be logged (such as PII or PHI).
* You are vulnerable to injections or attacks on the logging or monitoring systems if log data is not correctly encoded.
* The application is missing or mishandling errors and other exceptional conditions, such that the system is unaware there was an error, and is therefore unable to log there was a problem.
* Adequate ‘use cases’ for issuing alerts are missing or outdated to recognize a special situation.
* Too many false positive alerts make it impossible to distinguish important alerts from unimportant ones, resulting in them being recognized too late or not at all (physical overload of the SOC team).
* Detected alerts cannot be processed correctly because the playbook for the use case is incomplete, out of date, or missing.


## How to prevent.

Developers should implement some or all the following controls, depending on the risk of the application:


* Ensure all login, access control, and server-side input validation failures can be logged with sufficient user context to identify suspicious or malicious accounts and held for enough time to allow delayed forensic analysis.
* Ensure that every part of your app that contains a security control is logged, whether it succeeds or fails.
* Ensure that logs are generated in a format that log management solutions can easily consume.
* Ensure log data is encoded correctly to prevent injections or attacks on the logging or monitoring systems.
* Ensure all transactions have an audit trail with integrity controls to prevent tampering or deletion, such as append-only database tables or similar.
* Ensure all transactions that throw an error are rolled back and started over. Always fail closed.
* If your application or its users behave suspiciously, issue an alert. Create guidance for your developers on this topic so they can code against this or buy a system for this.
* DevSecOps and security teams should establish effective monitoring and alerting use cases including playbooks such that suspicious activities are detected and responded to quickly by the Security Operations Center (SOC) team.
* Add ‘honeytokens’ as traps for attackers into your application e.g. into the database, data, as real and/or technical user identity. As they are not used in normal business, any access generates logging data that can be alerted with nearly no false positives.
* Behavior analysis and AI support could be optionally an additional technique to support low rates of false positives for alerts.
* Establish or adopt an incident response and recovery plan, such as National Institute of Standards and Technology (NIST) 800-61r2 or later. Teach your software developers what application attacks and incidents look like, so they can report them.

There are commercial and open-source application protection products such as the OWASP ModSecurity Core Rule Set, and open-source log correlation software, such as the Elasticsearch, Logstash, Kibana (ELK) stack, that feature custom dashboards and alerting that may help you combat these issues. There are also commercial observability tools that can help you respond to or block attacks in close to real-time.


## Example attack scenarios.

**Scenario #1:** A children's health plan provider's website operator couldn't detect a breach due to a lack of monitoring and logging. An external party informed the health plan provider that an attacker had accessed and modified thousands of sensitive health records of more than 3.5 million children. A post-incident review found that the website developers had not addressed significant vulnerabilities. As there was no logging or monitoring of the system, the data breach could have been in progress since 2013, a period of more than seven years.

**Scenario #2:** A major Indian airline had a data breach involving more than ten years' worth of personal data of millions of passengers, including passport and credit card data. The data breach occurred at a third-party cloud hosting provider, who notified the airline of the breach after some time.

**Scenario #3:** A major European airline suffered a GDPR reportable breach. The breach was reportedly caused by payment application security vulnerabilities exploited by attackers, who harvested more than 400,000 customer payment records. The airline was fined 20 million pounds as a result by the privacy regulator.


## References.

-   [OWASP Proactive Controls: C9: Implement Logging and Monitoring](https://top10proactive.owasp.org/archive/2024/the-top-10/c9-security-logging-and-monitoring/)

-   [OWASP Application Security Verification Standard: V16 Security Logging and Error Handling](https://github.com/OWASP/ASVS/blob/v5.0.0/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md)

-   [OWASP Cheat Sheet: Application Logging Vocabulary](https://cheatsheetseries.owasp.org/cheatsheets/Application_Logging_Vocabulary_Cheat_Sheet.html)

-   [OWASP Cheat Sheet: Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

-   [Data Integrity: Recovering from Ransomware and Other Destructive Events](https://csrc.nist.gov/publications/detail/sp/1800-11/final)

-   [Data Integrity: Identifying and Protecting Assets Against Ransomware and Other Destructive Events](https://csrc.nist.gov/publications/detail/sp/1800-25/final)

-   [Data Integrity: Detecting and Responding to Ransomware and Other Destructive Events](https://csrc.nist.gov/publications/detail/sp/1800-26/final)

-   [Real world example of such failures in Snowflake Breach](https://www.huntress.com/threat-library/data-breach/snowflake-data-breach)


## List of Mapped CWEs

* [CWE-117 Improper Output Neutralization for Logs](https://cwe.mitre.org/data/definitions/117.html)

* [CWE-221 Information Loss of Omission](https://cwe.mitre.org/data/definitions/221.html)

* [CWE-223 Omission of Security-relevant Information](https://cwe.mitre.org/data/definitions/223.html)

* [CWE-532 Insertion of Sensitive Information into Log File](https://cwe.mitre.org/data/definitions/532.html)

* [CWE-778 Insufficient Logging](https://cwe.mitre.org/data/definitions/778.html)

---

## Section 11: A10 2025-Mishandling Of Exceptional Conditions

# A10:2025 Mishandling of Exceptional Conditions ![icon](../assets/TOP_10_Icons_Final_Mishandling_of_Exceptional_Conditions.png){: style="height:80px;width:80px" align="right"}


## Background. 

Mishandling of Exceptional Conditions is a new category for 2025. This category contains 24 CWEs and focuses on improper error handling, logical errors, failing open, and other related scenarios stemming from abnormal conditions and systems may encounter. This category has some CWEs that were previously associated with poor code quality. That was too general for us; in our opinion, this more specific category provides better guidance.

Notable CWEs included in this category: *CWE-209 Generation of Error Message Containing Sensitive Information, CWE-234 Failure to Handle Missing Parameter, CWE-274 Improper Handling of Insufficient Privileges, CWE-476 NULL Pointer Dereference,* and *CWE-636 Not Failing Securely ('Failing Open')*.


## Score table.


<table>
  <tr>
   <td>CWEs Mapped 
   </td>
   <td>Max Incidence Rate
   </td>
   <td>Avg Incidence Rate
   </td>
   <td>Max Coverage
   </td>
   <td>Avg Coverage
   </td>
   <td>Avg Weighted Exploit
   </td>
   <td>Avg Weighted Impact
   </td>
   <td>Total Occurrences
   </td>
   <td>Total CVEs
   </td>
  </tr>
  <tr>
   <td>24
   </td>
   <td>20.67%
   </td>
   <td>2.95%
   </td>
   <td>100.00%
   </td>
   <td>37.95%
   </td>
   <td>7.11
   </td>
   <td>3.81
   </td>
   <td>769,581
   </td>
   <td>3,416
   </td>
  </tr>
</table>



## Description. 

Mishandling exceptional conditions in software happens when programs fail to prevent, detect, and respond to unusual and unpredictable situations, which leads to crashes, unexpected behavior, and sometimes vulnerabilities. This can involve one or more of the following 3 failings; the application doesn’t prevent an unusual situation from happening, it doesn’t identify the situation as it is happening, and/or it responds poorly or not at all to the situation afterwards.

 

Exceptional conditions can be caused by missing, poor, or incomplete input validation, or late, high level error handling instead at the functions where they occur, or unexpected environmental states such as memory, privilege, or network issues, inconsistent exception handling, or exceptions that are not handled at all, allowing the system to fall into an unknown and unpredictable state. Any time an application is unsure of its next instruction, an exceptional condition has been mishandled. Hard-to-find errors and exceptions can threaten the security of the whole application for a long time.

 

Many different security vulnerabilities can happen when we mishandle exceptional conditions,

such as logic bugs, overflows, race conditions, fraudulent transactions, or issues with memory, state, resource, timing, authentication, and authorization. These types of vulnerabilities can negatively affect the confidentiality, availability, and/or integrity of a system or it’s data. Attackers manipulate an application's flawed error handling to strike this vulnerability. 


## How to prevent. 

In order to handle an exceptional condition properly we must plan for such situations (expect the worst). We must ‘catch’ every possible system error directly at the place where they occur and then handle it (which means do something meaningful to solve the problem and ensure we recover from the issue). As part of the handling, we should include throwing an error (to inform the user in an understandable way), logging of the event, as well as issuing an alert if we feel that is justified. We should also have a global exception handler in place in case there is ever something we have missed. Ideally, we would also have monitoring and/or observability tooling or functionality that watches for repeated errors or patterns that indicate an on-going attack, that could issue a response, defense, or blocking of some kind. This can help us block and respond to scripts and bots that focus on our error handling weaknesses.

 

Catching and handling exceptional conditions ensures that the underlying infrastructure of our programs are not left to deal with unpredictable situations. If you are part way through a transaction of any kind, it is extremely important that you roll back every part of the transaction and start again (also known as failing closed). Attempting to recover a transaction part way through is often where we create unrecoverable mistakes.

 

Whenever possible, add rate limiting, resource quotas, throttling, and other limits wherever possible, to prevent exceptional conditions in the first place. Nothing in information technology should be limitless, as this leads to a lack of application resilience, denial of service, successful brute force attacks, and extraordinary cloud bills. 

Consider whether identical repeated errors, above a certain rate, should only be outputted as statistics showing how often they have occurred and in what time frame. This information should be appended to the original message so as not to interfere with automated logging and monitoring, see [A09:2025 Security Logging & Alerting Failures](A09_2025-Security_Logging_and_Alerting_Failures.md).

On top of this, we would want to include strict input validation (with sanitization or escaping for potentially hazardous characters that we must accept), and *centralized* error handling, logging, monitoring, and alerting, and a global exception handler. One application should not multiple functions for handling exceptional conditions, it should be performed in one place, the same way each time. We should also create project security requirements for all the advice in this section, perform threat modelling and/or secure design review activities in the design phase of our projects, perform code review or static analysis, as well as execute stress, performance, and penetration testing of the final system.

 

If possible, your entire organization should handle exceptional conditions in the same way, as it makes it easier to review and audit code for errors in this important security control.


## Example attack scenarios. 

**Scenario #1:** Resource exhaustion via mishandling of exceptional conditions (Denial of Service) could be caused if the application catches exceptions when files are uploaded, but doesn’t properly release resources after. Each new exception leaves resources locked or otherwise unavailable, until all resources are used up.

**Scenario #2:** Sensitive data exposure via improper handling or database errors that reveals the full system error to the user. The attacker continues to force errors in order to use the sensitive system information to create a better SQL injection attack. The sensitive data in the user error messages are reconnaissance.

**Scenario #3:** State corruption in financial transactions could be caused by an attacker interrupting a multi-step transaction via network disruptions. Imagine the transaction order was: debit user account, credit destination account, log transaction. If the system doesn’t properly roll back the entire transaction (fail closed) when there is an error part way through, the attacker could potentially drain the user’s account, or possibly a race condition that allows the attacker to send money to the destination multiple times.


## References.

OWASP MASVS‑RESILIENCE

- [OWASP Cheat Sheet: Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

- [OWASP Cheat Sheet: Error Handling](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)

- [OWASP Application Security Verification Standard (ASVS): V16.5 Error Handling](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md#v165-error-handling)

- [OWASP Testing Guide: 4.8.1 Testing for Error Handling](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/01-Testing_For_Improper_Error_Handling)

* [Best practices for exceptions (Microsoft, .Net)](https://learn.microsoft.com/en-us/dotnet/standard/exceptions/best-practices-for-exceptions)

* [Clean Code and the Art of Exception Handling (Toptal)](https://www.toptal.com/developers/abap/clean-code-and-the-art-of-exception-handling)

* [General error handling rules (Google for Developers)](https://developers.google.com/tech-writing/error-messages/error-handling)

* [Example of real-world mishandling of an exceptional condition](https://www.firstreference.com/blog/human-error-and-internal-control-failures-cause-us62m-fine/) 

## List of Mapped CWEs
* [CWE-209	Generation of Error Message Containing Sensitive Information](https://cwe.mitre.org/data/definitions/209.html)
* [CWE-215	Insertion of Sensitive Information Into Debugging Code](https://cwe.mitre.org/data/definitions/215.html)
* [CWE-234	Failure to Handle Missing Parameter](https://cwe.mitre.org/data/definitions/234.html)
* [CWE-235	Improper Handling of Extra Parameters](https://cwe.mitre.org/data/definitions/235.html)
* [CWE-248	Uncaught Exception](https://cwe.mitre.org/data/definitions/248.html)
* [CWE-252	Unchecked Return Value](https://cwe.mitre.org/data/definitions/252.html)
* [CWE-274	Improper Handling of Insufficient Privileges](https://cwe.mitre.org/data/definitions/274.html)
* [CWE-280	Improper Handling of Insufficient Permissions or Privileges](https://cwe.mitre.org/data/definitions/280.html)
* [CWE-369	Divide By Zero](https://cwe.mitre.org/data/definitions/369.html)
* [CWE-390	Detection of Error Condition Without Action](https://cwe.mitre.org/data/definitions/390.html)
* [CWE-391	Unchecked Error Condition](https://cwe.mitre.org/data/definitions/391.html)
* [CWE-394	Unexpected Status Code or Return Value](https://cwe.mitre.org/data/definitions/394.html)
* [CWE-396	Declaration of Catch for Generic Exception](https://cwe.mitre.org/data/definitions/396.html)
* [CWE-397	Declaration of Throws for Generic Exception](https://cwe.mitre.org/data/definitions/397.html)
* [CWE-460	Improper Cleanup on Thrown Exception](https://cwe.mitre.org/data/definitions/460.html)
* [CWE-476	NULL Pointer Dereference](https://cwe.mitre.org/data/definitions/476.html)
* [CWE-478	Missing Default Case in Multiple Condition Expression](https://cwe.mitre.org/data/definitions/478.html)
* [CWE-484	Omitted Break Statement in Switch](https://cwe.mitre.org/data/definitions/484.html)
* [CWE-550	Server-generated Error Message Containing Sensitive Information](https://cwe.mitre.org/data/definitions/550.html)
* [CWE-636	Not Failing Securely ('Failing Open')](https://cwe.mitre.org/data/definitions/636.html)
* [CWE-703	Improper Check or Handling of Exceptional Conditions](https://cwe.mitre.org/data/definitions/703.html)
* [CWE-754	Improper Check for Unusual or Exceptional Conditions](https://cwe.mitre.org/data/definitions/754.html)
* [CWE-755	Improper Handling of Exceptional Conditions](https://cwe.mitre.org/data/definitions/755.html)
* [CWE-756	Missing Custom Error Page](https://cwe.mitre.org/data/definitions/756.html)

---

## Section 12: Authentication Cheat Sheet

# Authentication Cheat Sheet

## Introduction

**Authentication** (**AuthN**) is the process of verifying that an individual, entity, or website is who or what it claims to be by determining the validity of one or more authenticators (like passwords, fingerprints, or security tokens) that are used to back up this claim.

**Digital Identity** is the unique representation of a subject engaged in an online transaction. A digital identity is always unique in the context of a digital service but does not necessarily need to be traceable back to a specific real-life subject.

**Identity Proofing** establishes that a subject is actually who they claim to be. This concept is related to KYC concepts and it aims to bind a digital identity with a real person.

**Session Management** is a process by which a server maintains the state of an entity interacting with it. This is required for a server to remember how to react to subsequent requests throughout a transaction. Sessions are maintained on the server by a session identifier which can be passed back and forth between the client and server when transmitting and receiving requests. Sessions should be unique per user and computationally very difficult to predict. The [Session Management Cheat Sheet](Session_Management_Cheat_Sheet.md) contains further guidance on the best practices in this area.

## Authentication General Guidelines

### User IDs

The primary function of a User ID is to uniquely identify a user within a system. Ideally, User IDs should be randomly generated to prevent the creation of predictable or sequential IDs, which could pose a security risk, especially in systems where User IDs might be exposed or inferred from external sources.

### Usernames

Usernames are easy-to-remember identifiers chosen by the user and used for identifying themselves when logging into a system or service. The terms User ID and username might be used interchangeably if the username chosen by the user also serves as their unique identifier within the system.

Users should be permitted to use their email address as a username, provided the email is verified during sign-up. Additionally, they should have the option to choose a username other than an email address. For information on validating email addresses, please visit the [input validation cheat sheet email discussion](Input_Validation_Cheat_Sheet.md#email-address-validation).

### Authentication Solution and Sensitive Accounts

- Do **NOT** allow login with sensitive accounts (i.e. accounts that can be used internally within the solution such as to a backend / middleware / database) to any front-end user interface
- Do **NOT** use the same authentication solution (e.g. IDP / AD) used internally for unsecured access (e.g., public access / DMZ)

### Implement Proper Password Strength Controls

A key concern when using passwords for authentication is password strength. A "strong" password policy makes it difficult or even improbable for one to guess the password through either manual or automated means. The following characteristics define a strong password:

- Password Length
    - **Minimum** length for passwords should be enforced by the application.
        - If MFA is enabled passwords **shorter than 8 characters** are considered to be weak ([NIST SP800-63B](https://pages.nist.gov/800-63-4/sp800-63b.html#passwordver)).
        - If MFA is not enabled passwords **shorter than 15 characters** are considered to be weak ([NIST SP800-63B](https://pages.nist.gov/800-63-4/sp800-63b.html#passwordver)).
    - **Maximum** password length should be **at least 64 characters** to allow passphrases ([NIST SP800-63B](https://pages.nist.gov/800-63-4/sp800-63b.html#passwordlength)). Note that certain implementations of hashing algorithms may cause [long password denial of service](https://www.acunetix.com/vulnerabilities/web/long-password-denial-of-service/).
    - Longer passphrases are effective because they raise the number of guesses an attacker's dictionary or wordlist has to cover, not because of a precise entropy value: NIST notes that "estimating entropy for user-chosen passwords is challenging" and recommends length and blocklist checks (see below) over composition or entropy math ([NIST SP800-63B, Strength of Passwords](https://pages.nist.gov/800-63-4/sp800-63b/passwords/#appA)). Entropy estimates rely on assumptions about the search space and should be treated as illustrative rather than as absolute measures of password strength.
    - Attackers commonly use password guessing techniques that leverage common-password dictionaries and password lists, and may use previously compromised credentials in credential stuffing attacks. These behaviors are reflected in [MITRE ATT&CK T1110 – Brute Force](https://attack.mitre.org/techniques/T1110/), including Password Guessing, Password Spraying, and Credential Stuffing. Screening passwords against blocklists helps prevent users from selecting passwords that are commonly used or already known to attackers, as recommended by [NIST SP 800-63B – Passwords](https://pages.nist.gov/800-63-4/sp800-63b/passwords/).
- Do not silently truncate passwords. The [Password Storage Cheat Sheet](Password_Storage_Cheat_Sheet.md#input-limits-of-bcrypt) provides further guidance on how to handle passwords that are longer than the maximum length.
- Allow usage of **all** characters including unicode and whitespace. There should be no password composition rules limiting the type of characters permitted. There should be no requirement for upper or lower case or numbers or special characters.
- Ensure credential rotation when a password leak occurs, at the time of compromise identification or when authenticator technology changes. Avoid requiring periodic password changes; instead, encourage users to pick strong passwords and enable [Multifactor Authentication Cheat Sheet (MFA)](Multifactor_Authentication_Cheat_Sheet.md). According to NIST guidelines, verifiers should not mandate arbitrary password changes (e.g., periodically).
- Include a password strength meter to help users create a more complex password
    - [zxcvbn-ts library](https://github.com/zxcvbn-ts/zxcvbn) can be used for this purpose.
    - Other language implementations of zxcvbn [listed here](https://github.com/dropbox/zxcvbn?tab=readme-ov-file); however check the age and maturity of each example before use.
- Block common and previously breached passwords
    - [Pwned Passwords](https://haveibeenpwned.com/Passwords) is a service where passwords can be checked against previously breached passwords. Details on the API [are here](https://haveibeenpwned.com/API/v3#PwnedPasswords).
    - Alternatively, you can download the [Pwned Passwords](https://haveibeenpwned.com/Passwords) database [using this mechanism](https://github.com/HaveIBeenPwned/PwnedPasswordsDownloader?tab=readme-ov-file#what-is-haveibeenpwned-downloader) to host it yourself.
    - Other top password lists are available but there is no guarantee as to how updated they are:
        - [Various password lists](https://github.com/danielmiessler/SecLists/tree/master/Passwords) hosted by SecLists from Daniel Miessler.

#### For more detailed information check

- [ASVS v5.0 Password Security Requirements](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md#v62-password-security)
- [Passwords Evolved: Authentication Guidance for the Modern Era](https://www.troyhunt.com/passwords-evolved-authentication-guidance-for-the-modern-era/)

### Implement Secure Password Recovery Mechanism

It is common for an application to have a mechanism that provides a means for a user to gain access to their account in the event they forget their password. Please see [Forgot Password Cheat Sheet](Forgot_Password_Cheat_Sheet.md) for details on this feature.

### Store Passwords in a Secure Fashion

It is critical for an application to store a password using the right cryptographic technique. Please see [Password Storage Cheat Sheet](Password_Storage_Cheat_Sheet.md) for details on this feature.

### Compare Password Hashes Using Safe Functions

Where possible, the user-supplied password should be compared to the stored password hash using a secure password comparison function provided by the language or framework, such as the [password_verify()](https://www.php.net/manual/en/function.password-verify.php) function in PHP. Where this is not possible, ensure that the comparison function:

- Has a maximum input length, to protect against denial of service attacks with very long inputs.
- Explicitly sets the type of both variables, to protect against type confusion attacks such as Magic Hashes in PHP.
- Returns in constant time, to protect against timing attacks.

### Change Password Feature

When developing a change password feature, ensure to have:

- The user is authenticated with an active session.
- Current password verification. This is to ensure that it's the legitimate user who is changing the password. Consider this abuse case: a user logs in on a public computer and forgets to log out. Another person could then use that active session. If we don't verify the current password, this other person may be able to change the password.

### Transmit Passwords Only Over TLS or Other Strong Transport

See: [Transport Layer Security Cheat Sheet](Transport_Layer_Security_Cheat_Sheet.md)

The login page and all subsequent authenticated pages must be exclusively accessed over TLS or other strong transport. Failure to utilize TLS or other strong transport for the login page allows an attacker to modify the login form action, causing the user's credentials to be posted to an arbitrary location. Failure to utilize TLS or other strong transport for authenticated pages after login enables an attacker to view the unencrypted session ID and compromise the user's authenticated session.

### Require Re-authentication for Sensitive Features

In order to mitigate CSRF and session hijacking, it's important to require the current credentials for an account before updating sensitive account information such as the user's password or email address -- or before sensitive transactions, such as shipping a purchase to a new address. Without this countermeasure, an attacker may be able to execute sensitive transactions through a CSRF or XSS attack without needing to know the user's current credentials. Additionally, an attacker may get temporary physical access to a user's browser or steal their session ID to take over the user's session.

### Re-authentication After Risk Events

**Overview:**
Re-authentication is critical when an account has experienced high-risk activity such as account recovery, password resets, or suspicious behavior patterns. This section outlines when and how to trigger re-authentication to protect users and prevent unauthorized access. For further details, see the [Require Re-authentication for Sensitive Features](#require-re-authentication-for-sensitive-features) section.

#### When to Trigger Re-authentication

- **Suspicious Account Activity**
  When unusual login patterns, IP address changes, or device enrollments occur
- **Account Recovery**
  After users reset their passwords or change sensitive account details
- **Critical Actions**
  For high-risk actions like changing payment details or adding new trusted devices

#### Re-authentication Mechanisms

- **Adaptive Authentication**
  Use risk-based authentication models that adapt to the user's behavior and context
- **Multi-Factor Authentication (MFA)**
  Require an additional layer of verification for sensitive actions or events
- **Bound Authenticators**
  Require an authenticator already bound to the account, such as the current password or a passkey. Do not substitute security questions, which are excluded by [ASVS 6.4.2](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md#v64-authentication-factor-lifecycle-and-recovery).

#### Implementation Recommendations

- **Minimize User Friction**
  Ensure that re-authentication does not disrupt the user experience unnecessarily
- **Context-Aware Decisions**
  Make re-authentication decisions based on context (e.g., geolocation, device type, prior patterns)
- **Secure Session Management**
  Invalidate sessions after re-authentication and rotate tokens—see the [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)

### Consider Strong Transaction Authentication

Some applications should use a second factor to check whether a user may perform sensitive operations. For more information, see the [Transaction Authorization Cheat Sheet](Transaction_Authorization_Cheat_Sheet.md).

#### TLS Client Authentication

TLS Client Authentication, also known as two-way TLS authentication, consists of both browser and server sending their respective TLS certificates during the TLS handshake process. Just as you can validate the authenticity of a server by using the certificate and asking a verifiably-valid Certificate Authority (CA) if the certificate is valid, the server can authenticate the user by receiving a certificate from the client and validating against a third-party CA or its own CA. To do this, the server must provide the user with a certificate generated specifically for him, assigning values to the subject so that these can be used to determine what user the certificate should validate. The user installs the certificate on a browser and now uses it for the website.

This approach is appropriate when:

- It is acceptable (or even preferred) that the user has access to the website only from a single computer/browser.
- The user is not easily scared by the process of installing TLS certificates on their browser, or there will be someone, probably from IT support, who will do this for the user.
- The website requires an extra step of security.
- It is also a good thing to use when the website is for an intranet of a company or organization.

It is generally not a good idea to use this method for widely and publicly available websites that will have an average user. For example, it wouldn't be a good idea to implement this for a website like Facebook. While this technique can prevent the user from having to type a password (thus protecting against an average keylogger from stealing it), it is still considered a good idea to consider using both a password and TLS client authentication combined.

Additionally, if the client is behind an enterprise proxy that performs SSL/TLS decryption, this will break certificate authentication unless the site is allowed on the proxy.

For more information, see: [Client-authenticated TLS handshake](https://en.wikipedia.org/wiki/Transport_Layer_Security#Client-authenticated_TLS_handshake)

### Authentication and Error Messages

Incorrectly implemented error messages in the case of authentication functionality can be used for the purposes of user ID and password enumeration. An application should respond (both HTTP and HTML) in a generic manner.

#### Authentication Responses

Using any of the authentication mechanisms (login, password reset, or password recovery), an application must respond with a generic error message regardless of whether:

- The user ID or password was incorrect.
- The account does not exist.
- The account is locked or disabled.

The account registration feature should also be taken into consideration, and the same approach of a generic error message can be applied regarding the case in which the user exists.

The objective is to prevent the creation of a [discrepancy factor](https://cwe.mitre.org/data/definitions/204.html), allowing an attacker to mount a user enumeration action against the application.

It is interesting to note that the business logic itself can bring a discrepancy factor related to the processing time taken. Indeed, depending on the implementation, the processing time can be significantly different according to the case (success vs failure) allowing an attacker to mount a [time-based attack](https://en.wikipedia.org/wiki/Timing_attack) (delta of some seconds for example).

Example using pseudo-code for a login feature:

- First implementation using the "quick exit" approach

```text
IF USER_EXISTS(username) THEN
    password_hash=HASH(password)
    IS_VALID=LOOKUP_CREDENTIALS_IN_STORE(username, password_hash)
    IF NOT IS_VALID THEN
        RETURN Error("Invalid Username or Password!")
    ENDIF
ELSE
   RETURN Error("Invalid Username or Password!")
ENDIF
```

It can be clearly seen that if the user doesn't exist, the application will directly throw an error. Otherwise, when the user exists and the password doesn't, it is apparent that there will be more processing before the application errors out. In return, the response time will be different for the same error, allowing the attacker to differentiate between a wrong username and a wrong password.

- Second implementation without relying on the "quick exit" approach:

```text
password_hash=HASH(password)
IS_VALID=LOOKUP_CREDENTIALS_IN_STORE(username, password_hash)
IF NOT IS_VALID THEN
   RETURN Error("Invalid Username or Password!")
ENDIF
```

This code will go through the same process no matter what the user or the password is, allowing the application to return in approximately the same response time.

The problem with returning a generic error message for the user is a User Experience (UX) matter. A legitimate user might feel confused with the generic messages, thus making it hard for them to use the application, and might after several retries, leave the application because of its complexity. The decision to return a *generic error message* can be determined based on the criticality of the application and its data. For example, for critical applications, the team can decide that under the failure scenario, a user will always be redirected to the support page and a *generic error message* will be returned.

Regarding the user enumeration itself, protection against [brute-force attacks](#protect-against-automated-attacks) is also effective because it prevents an attacker from applying the enumeration at scale. Usage of [CAPTCHA](https://en.wikipedia.org/wiki/CAPTCHA) can be applied to a feature for which a *generic error message* cannot be returned because the *user experience* must be preserved.

##### Incorrect and correct response examples

###### Login

Incorrect response examples:

- "Login for User foo: invalid password."
- "Login failed, invalid user ID."
- "Login failed; account disabled."
- "Login failed; this user is not active."

Correct response example:

- "Login failed; Invalid user ID or password."

###### Password recovery

Incorrect response examples:

- "We just sent you a password reset link."
- "This email address doesn't exist in our database."

Correct response example:

- "If that email address is in our database, we will send you an email to reset your password."

###### Account creation

Incorrect response examples:

- "This user ID is already in use."
- "Welcome! You have signed up successfully."

Correct response example:

- "A link to activate your account has been emailed to the address provided."

##### Error Codes and URLs

The application may return a different [HTTP Error code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) depending on the authentication attempt response. It may respond with a 200 for a positive result and a 403 for a negative result. Even though a generic error page is shown to a user, the HTTP response code may differ which can leak information about whether the account is valid or not.

Error disclosure can also be used as a discrepancy factor, consult the [error handling cheat sheet](Error_Handling_Cheat_Sheet.md) regarding the global handling of different errors in an application.

### Protect Against Automated Attacks

There are a number of different types of automated attacks that attackers can use to try and compromise user accounts. The most common types are listed below:

| Attack Type         | Description                                                                                      |
|---------------------|--------------------------------------------------------------------------------------------------|
| Brute Force         | Testing multiple passwords from a dictionary or other source against a single account.           |
| Credential Stuffing | Testing username/password pairs obtained from the breach of another site.                        |
| Password Spraying   | Testing a single weak password against a large number of different accounts.                     |

Different protection mechanisms can be implemented to protect against these attacks. In many cases, these defenses do not provide complete protection, but when a number of them are implemented in a defense-in-depth approach, a reasonable level of protection can be achieved.

The following sections will focus primarily on preventing brute-force attacks, although these controls can also be effective against other types of attacks. For further guidance on defending against credential stuffing and password spraying, see the [Credential Stuffing Cheat Sheet](Credential_Stuffing_Prevention_Cheat_Sheet.md).

#### Multi-Factor Authentication

Multi-factor authentication (MFA) is by far the best defense against the majority of password-related attacks, including brute-force attacks, with analysis by Microsoft suggesting that it would have stopped [99.9% of account compromises](https://techcommunity.microsoft.com/t5/Azure-Active-Directory-Identity/Your-Pa-word-doesn-t-matter/ba-p/731984). As such, it should be implemented wherever possible; however, depending on the audience of the application, it may not be practical or feasible to enforce the use of MFA.

The [Multifactor Authentication Cheat Sheet](Multifactor_Authentication_Cheat_Sheet.md) contains further guidance on implementing MFA.

#### Login Throttling

Login Throttling is a security mechanism used to prevent an attacker from making too many attempts at guessing a password through normal interactive means, it includes the following controls:

- Maximum number of attempts.

##### Account Lockout

The most common protection against these attacks is to implement account lockout, which prevents any more login attempts for a period after a certain number of failed logins.

The counter of failed logins should be associated with the account itself, rather than the source IP address, in order to prevent an attacker from making login attempts from a large number of different IP addresses. There are a number of different factors that should be considered when implementing an account lockout policy in order to find a balance between security and usability:

- The number of failed attempts before the account is locked out (lockout threshold).
- The time period that these attempts must occur within (observation window).
- How long the account is locked out for (lockout duration).

Rather than implementing a fixed lockout duration (e.g., ten minutes), some applications use an exponential lockout, where the lockout duration starts as a very short period (e.g., one second), but doubles after each failed login attempt.

- Amount of time to delay after each account lockout (max 2-3, after that permanent account lockout).

When designing an account lockout system, care must be taken to prevent it from being used to cause a denial of service by locking out other users' accounts. One way this could be performed is to allow the use of the forgotten password functionality to log in, even if the account is locked out.

#### CAPTCHA

The use of an effective CAPTCHA can help to prevent automated login attempts against accounts. However, many CAPTCHA implementations have weaknesses that allow them to be solved using automated techniques or can be outsourced to services that can solve them. As such, the use of CAPTCHA should be viewed as a defense-in-depth control to make brute-force attacks more time-consuming and expensive, rather than as a preventative.

It may be more user-friendly to only require a CAPTCHA be solved after a small number of failed login attempts, rather than requiring it from the very first login.

#### Security Questions and Memorable Words

Do not use security questions for authentication or re-authentication; [ASVS 6.4.2](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md#v64-authentication-factor-lifecycle-and-recovery) excludes knowledge-based authentication. When verifying a password or memorable word, request and verify the full secret rather than selected characters, as required by [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html#passwordver). See the [Choosing and Using Security Questions Cheat Sheet](Choosing_and_Using_Security_Questions_Cheat_Sheet.md) for guidance limited to legacy systems.

## Logging and Monitoring

Enable logging and monitoring of authentication functions to detect attacks/failures on a real-time basis

- Ensure that all failures are logged and reviewed
- Ensure that all password failures are logged and reviewed
- Ensure that all account lockouts are logged and reviewed

## Use of authentication protocols that require no password

While authentication through a combination of username, password, and multi-factor authentication is considered generally secure, there are use cases where it isn't considered the best option or even safe. Examples of this are third-party applications that desire to connect to the web application, either from a mobile device, another website, desktop, or other situations. When this happens, it is NOT considered safe to allow the third-party application to store the user/password combo, since then it extends the attack surface into their hands, where it isn't in your control. For this and other use cases, there are several authentication protocols that can protect you from exposing your users' data to attackers.

### OAuth 2.0 and 2.1

OAuth is an **authorization** framework for delegated access to APIs. See also: [OAuth 2.0 Cheat Sheet](OAuth2_Cheat_Sheet.md).

> **Note:** OAuth 2.1 is an active IETF Working Group draft that consolidates OAuth 2.0 and widely adopted best practices and is intended to replace RFC 6749/6750; guidance in this cheat sheet applies to both OAuth 2.0 and OAuth 2.1. Because Internet-Drafts are revisioned, use the [unversioned OAuth 2.1 Datatracker page](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/) for the current draft. See also [oauth.net/2.1](https://oauth.net/2.1/).

### OpenID Connect (OIDC)

**OpenID Connect 1.0 (OIDC)** is an identity layer **on top of OAuth**. It defines how a client (**relying party**) verifies the **end user's** identity using an **ID Token** (a signed JWT) and how to obtain user claims in an interoperable way. Use **OIDC for authentication/SSO**; use **OAuth for authorization** to APIs.

#### OIDC implementation guidance

- **Validate ID Tokens** on the relying party: issuer (`iss`), audience (`aud`), signature (per provider JWKs), expiration (`exp`).
- Prefer **well-maintained libraries/SDKs** and provider discovery/JWKS endpoints.
- Use the **UserInfo** endpoint when additional claims beyond the ID Token are required.

> **Avoid confusion:** **OpenID 2.0 ("OpenID")** was a separate, legacy authentication protocol that has been **superseded by OpenID Connect** and is considered obsolete. New systems should not implement OpenID 2.0. References: [OpenID Foundation — obsolete OpenID 2.0 libraries](https://openid.net/developers/libraries-for-obsolete-specifications/), [OpenID 2.0 → OIDC migration](https://openid.net/specs/openid-connect-migration-1_0.html)

#### Secure Federated Account Linking

When linking an OIDC identity to an existing application account:

- Identify the federated identity using the combination of `iss` (issuer) and `sub` (subject), not `sub` alone. See [OIDC claim stability and uniqueness](https://openid.net/specs/openid-connect-core-1_0.html#ClaimStability).
- Do not automatically link accounts solely because their `email`, `preferred_username`, or other profile attributes match. These claims are not guaranteed to be unique or stable, as explained in [OIDC Core Section 5.7](https://openid.net/specs/openid-connect-core-1_0.html#ClaimStability).
- Require an authenticated session with the existing application account before adding or removing linked identities, as described in [NIST SP 800-63C-4, Section 3.8.1](https://pages.nist.gov/800-63-4/sp800-63c/Federation/). Apply the guidance in [Require Re-authentication for Sensitive Features](#require-re-authentication-for-sensitive-features) before changing account links.
- Authenticate the identity being added and [validate the resulting ID Token](https://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation) before saving the link. Bind the authentication response to the user's linking session using the protections described in the [OAuth 2.0 Cheat Sheet](OAuth2_Cheat_Sheet.md).
- After unlinking, disallow access to the application account through the removed identity. See [NIST SP 800-63C-4, Section 3.8.1](https://pages.nist.gov/800-63-4/sp800-63c/Federation/).
- Notify the user when an identity is added, or when an identity is removed without terminating the application account, as described in [NIST SP 800-63C-4, Section 3.8](https://pages.nist.gov/800-63-4/sp800-63c/Federation/).

### SAML

Security Assertion Markup Language (SAML) is often considered to compete with OpenId. The most recommended version is 2.0 since it is very feature-complete and provides strong security. Like OpenId, SAML uses identity providers, but unlike OpenId, it is XML-based and provides more flexibility. SAML is based on browser redirects which send XML data. Furthermore, SAML isn't only initiated by a service provider; it can also be initiated from the identity provider. This allows the user to navigate through different portals while still being authenticated without having to do anything, making the process transparent.

While OpenId has taken most of the consumer market, SAML is often the choice for enterprise applications because there are few OpenId identity providers which are considered enterprise-class (meaning that the way they validate the user identity doesn't have high standards required for enterprise identity). It is more common to see SAML being used inside of intranet websites, sometimes even using a server from the intranet as the identity provider.

In the past few years, applications like SAP ERP and SharePoint (SharePoint by using Active Directory Federation Services 2.0) have decided to use SAML 2.0 authentication as an often preferred method for single sign-on implementations whenever enterprise federation is required for web services and web applications.

**See also: [SAML Security Cheat Sheet](SAML_Security_Cheat_Sheet.md)**

### FIDO

The Fast Identity Online (FIDO) Alliance has created two protocols to facilitate online authentication: the Universal Authentication Framework (UAF) protocol and the Universal Second Factor (U2F) protocol. While UAF focuses on passwordless authentication, U2F allows the addition of a second factor to existing password-based authentication. Both protocols are based on a public key cryptography challenge-response model.

UAF takes advantage of existing security technologies present on devices for authentication including fingerprint sensors, cameras (face biometrics), microphones (voice biometrics), Trusted Execution Environments (TEEs), Secure Elements (SEs), and others. The protocol is designed to plug these device capabilities into a common authentication framework. UAF works with both native applications and web applications.

U2F augments password-based authentication using a hardware token (typically USB) that stores cryptographic authentication keys and uses them for signing. The user can use the same token as a second factor for multiple applications. U2F works with web applications. It provides **protection against phishing** by using the URL of the website to look up the stored authentication key.

**FIDO2**: [FIDO2 combines WebAuthn with the Client-to-Authenticator Protocols (CTAP)](https://fidoalliance.org/specifications/). U2F is now named CTAP1; UAF is a separate protocol. WebAuthn credentials form the foundation of modern **Passkeys** technology. Passkeys enable users to securely log in using local user verification (such as biometrics or device PINs), often with credential synchronization across devices.

#### Hardware-backed Key Storage

For many authenticators, including common platform passkeys, the private key is generated and stored by the operating system's secure key manager. Depending on the platform and authenticator, keys may be protected using hardware-backed components such as the Trusted Platform Module (TPM) on Windows, Secure Enclave on Apple devices, or the Android Keystore/StrongBox on Android, or by other software-based mechanisms.

In typical implementations, the private key is intended to be non-exportable and bound to the authenticator, and the platform security module signs a server challenge using this key. However, some authenticators support credential synchronization or backup that may involve export or server-side storage, and not all implementations are hardware-backed. Relying parties should not assume that keys are hardware-backed and non-exportable unless this is verified (for example, via authenticator properties or attestation).

## Password Managers

Password managers are programs, browser plugins, or web services that automate the management of a large quantity of different credentials. Most password managers have functionality to allow users to easily use them on websites, either:
(a) by pasting the passwords into the login form
-- or --
(b) by simulating the user typing them in.

Web applications should not make the job of password managers more difficult than necessary by observing the following recommendations:

- Use standard HTML forms for username and password input with appropriate `type` attributes.
- Avoid plugin-based login pages (such as Flash or Silverlight).
- Implement a reasonable maximum password length, at least 64 characters, as discussed in the [Implement Proper Password Strength Controls section](#implement-proper-password-strength-controls).
- Allow any printable characters to be used in passwords.
- Allow users to paste into the username, password, and MFA fields.
- Allow users to navigate between the username and password field with a single press of the `Tab` key.

## Changing A User's Registered Email Address

User email addresses often change. The following process is recommended to handle such situations in a system:

*Note: The process is less stringent with [Multifactor Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html), as proof-of-identity is stronger than relying solely on a password.*

### Recommended Process If the User HAS [Multifactor Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html) Enabled

1. Confirm the validity of the user's authentication cookie/token. If not valid, display a login screen.
2. Describe the process for changing the registered email address to the user.
3. Ask the user to submit a proposed new email address, ensuring it complies with system rules.
4. Request the use of [Multifactor Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html) for identity verification.
5. Store the proposed new email address as a pending change.
6. Create and store **two** time-limited nonces for (a) system administrators' notification, and (b) user confirmation.
7. Send two email messages with links that include those nonces:

    - A **notification-only email message** to the current address, alerting the user to the impending change and providing a link to report unexpected activity.

    - A **confirmation-required email message** to the proposed new address, instructing the user to confirm the change and providing a link for unexpected situations.

8. Handle responses from the links accordingly.

### Recommended Process If the User DOES NOT HAVE Multifactor Authentication Enabled

1. Confirm the validity of the user's authentication cookie/token. If not valid, display a login screen.
2. Describe the process for changing the registered email address to the user.
3. Ask the user to submit a proposed new email address, ensuring it complies with system rules.
4. Request the user's current password for identity verification.
5. Store the proposed new email address as a pending change.
6. Create and store three time-limited nonces for system administrators' notification, user confirmation, and an additional step for password reliance.
7. Send two email messages with links to those nonces:

    - A **confirmation-required email message** to the current address, instructing the user to confirm the change and providing a link for an unexpected situation.

    - A **separate confirmation-required email message** to the proposed new address, instructing the user to confirm the change and providing a link for unexpected situations.

8. Handle responses from the links accordingly.

### Notes on the Above Processes

- It's worth noting that Google adopts a different approach with accounts secured only by a password -- [where the current email address receives a notification-only email](https://support.google.com/accounts/answer/55393?hl=en). This method carries risks and requires user vigilance.

- Regular social engineering training is crucial. System administrators and help desk staff should be trained to follow the prescribed process and recognize and respond to social engineering attacks. Refer to [CISA's "Avoiding Social Engineering and Phishing Attacks"](https://www.cisa.gov/news-events/news/avoiding-social-engineering-and-phishing-attacks) for guidance.

## Adaptive or Risk Based Authentication

A feature of more advanced applications is the ability to require different authentication stages depending on various environmental and contextual attributes (including but not limited to, the sensitivity of the data for which access is being requested, time of day, user location, IP address, or device fingerprint).

For example, an application may require MFA for the first login from a particular device but not for subsequent logins from that device. Alternatively, a single sign-on solution may authenticate the user and allow them to remain logged in for a day but require a reauthentication if they try to access their profile page.

Use device fingerprints, IP addresses, and remembered-device cookies as risk signals, not as substitutes for authentication. [NIST session guidance](https://pages.nist.gov/800-63-4/sp800-63b/session/) distinguishes an authenticated session secret from device and browser characteristics used for monitoring. Require authentication or a valid authenticated session before exposing private account data. For example, a banking application may allow balance viewing within an authenticated session and require stronger or fresher authentication for transaction details or money movement.

Questions that should be considered when implementing a mechanism like this include:

- Are the policies being put in place in line with any corporate policies and especially any regulatory policy?
- Which user‑ or device‑attributes (IP, geolocation, device fingerprint, time‑of‑day, behavioral biometrics, etc.) will we monitor at session start?
- Which of those signals need to be refreshed during an active session, and at what cadence?
- How will we ensure each signal’s accuracy and handle missing or low‑confidence data?
- What scoring model (weights, thresholds, ML, rule‑based, hybrid) will convert raw signals into a risk tier?
- Where will the model run (edge, API gateway, central service), and what is our latency budget?
- What action maps to each risk tier (allow, CAPTCHA, step‑up MFA, block, revoke session)?
- What user‑facing messages and error codes will accompany each action?
- At which exact code or platform layers will we invoke the risk engine (login controller, middleware, API gateway, service mesh)?
- How do we propagate decisions consistently across web, mobile, and API clients?
- How do we mutate, extend, or revoke tokens/cookies when a mid‑session risk check escalates?
- How do we synchronize state across multiple concurrent devices or browser tabs?
- What monitoring and alerting will be in place for potentially suspicious activity, including how the user is notified.

## References

- [NIST SP 800-63B-4: Password Verifiers](https://pages.nist.gov/800-63-4/sp800-63b.html#passwordver)
- [OWASP Application Security Verification Standard (ASVS): V6 Authentication](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md#v6-authentication)
- [OpenID Connect Core 1.0: ID Token Validation](https://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation)

---

## Section 13: Authorization Cheat Sheet

# Authorization Cheat Sheet

## Introduction

Authorization may be defined as "the process of verifying that a requested action or service is approved for a specific entity" ([NIST](https://csrc.nist.gov/glossary/term/authorization)). Authorization is distinct from authentication which is the process of verifying an entity's identity. When designing and developing a software solution, it is important to keep these distinctions in mind. A user who has been authenticated (perhaps by providing a username and password) is often not authorized to access every resource and perform every action that is technically possible through a system. For example, a web app may have both regular users and admins, with the admins being able to perform actions the average user is not privileged to perform, even though they have been authenticated. Additionally, authentication is not always required for accessing resources; an unauthenticated user may be authorized to access certain public resources, such as an image or login page, or even an entire web app.

The objective of this cheat sheet is to assist developers in implementing authorization logic that is robust, appropriate to the app's business context, maintainable, and scalable. The guidance provided in this cheat sheet should be applicable to all phases of the development lifecycle and flexible enough to meet the needs of diverse development environments.

Flaws related to authorization logic are a notable concern for web apps. Broken Access Control was ranked as the most concerning web security vulnerability in [OWASP's 2021 Top 10](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) and asserted to have a "High" likelihood of exploit by [MITRE's CWE program](https://cwe.mitre.org/data/definitions/285.html). Furthermore, according to [Veracode's State of Software Vol. 10](https://www.veracode.com/sites/default/files/pdf/resources/sossreports/state-of-software-security-volume-10-veracode-report.pdf), Access Control was among the more common of OWASP's Top 10 risks to be involved in exploits and security incidents despite being among the least prevalent of those examined.

The potential impact resulting from exploitation of authorization flaws is highly variable, both in form and severity. Attackers may be able to read, create, modify, or delete resources that were meant to be protected (thus jeopardizing their confidentiality, integrity, and/or availability); however, the actual impact of such actions is necessarily linked to the criticality and sensitivity of the compromised resources. Thus, the business cost of a successfully exploited authorization flaw can range from very low to extremely high.

Both entirely unauthenticated outsiders and authenticated (but not necessarily authorized) users can take advantage of authorization weaknesses.  Although honest mistakes or carelessness on the part of non-malicious entities may enable authorization bypasses, malicious intent is typically required for access control threats to be fully realized.  Horizontal privilege escalation (i.e. being able to access another user's resources) is an especially common weakness that an authenticated user may be able to take advantage of. Faults related to authorization control can allow malicious insiders and outsiders alike to view, modify, or delete sensitive resources of all forms (database records, static files, personally identifiable information (PII), etc.) or perform actions, such as creating a new account or initiating a costly order, that they should not be privileged to do. Furthermore, if logging related to access control is not properly set-up, such authorization violations may go undetected or at least remain unattributable to a particular individual or group.

## Recommendations

### Enforce Least Privileges

As a security concept, Least Privileges refers to the principle of assigning users only the minimum privileges necessary to complete their job. Although perhaps most commonly applied in system administration, this principle has relevance to the software developer as well. Least Privileges must be applied both horizontally and vertically. For example, even though both an accountant and sales representative may occupy the same level in an organization's hierarchy, both require access to different resources to perform their jobs. The accountant should likely not be granted access to a customer database and the sales representative should not be able to access payroll data. Similarly, the head of the sales department is likely to need more privileged access than their subordinates.

Failure to enforce least privileges in an application can jeopardize the confidentiality of sensitive resources. Mitigation strategies are applied primarily during the Architecture and Design phase (see [CWE-272](https://cwe.mitre.org/data/definitions/272.html)); however, the principle must be addressed throughout the SDLC.

Consider the following points and best practices:

- During the design phase, ensure trust boundaries are defined. Enumerate the types of users that will be accessing the system, the resources exposed and the operations (such as read, write, update, etc) that might be performed on those resources. For every combination of user type and resource, determine what operations, if any, the user (based on role and/or other attributes) must be able to perform on that resource. For an ABAC system ensure all categories of attributes are considered. For example, a Sales Representative may need to access a customer database from the internal network during working hours, but not from home at midnight.
- Create tests that validate that the permissions mapped out in the design phase are being correctly enforced.
- After the app has been deployed, periodically review permissions in the system for "privilege creep"; that is, ensure the privileges of users in the current environment do not exceed those defined during the design phase (plus or minus any formally approved changes).
- Remember, it is easier to grant users additional permissions rather than to take away some they previously enjoyed. Careful planning and implementation of Least Privileges early in the SDLC can help reduce the risk of needing to revoke permissions that are later deemed overly broad.

### Deny by Default

Even when no access control rules are explicitly matched, the application cannot remain neutral when an entity is requesting access to a particular resource. The application must always make a decision, whether implicitly or explicitly, to either deny or permit the requested access. Logic errors and other mistakes relating to access control may happen, especially when access requirements are complex; consequently, one should not rely entirely on explicitly defined rules for matching all possible requests. For security purposes an application should be configured to deny access by default.

Consider the following points and best practices:

- Adopt a "deny-by-default" mentality both during initial development and whenever new functionality or resources are exposed by the app. One should be able to explicitly justify why a specific permission was granted to a particular user or group rather than assuming access to be the default position.
- Although some frameworks or libraries may themselves adopt a deny-by-default strategy, explicit configuration should be preferred over relying on framework or library defaults. The logic and defaults of third-party code may evolve over time, without the developer's full knowledge or understanding of the change's implications for a particular project.
  
### Validate the Permissions on Every Request

Permission should be validated correctly on every request, regardless of whether the request was initiated by an AJAX script, server-side, or any other source. The technology used to perform such checks should allow for global, application-wide configuration rather than needing to be applied individually to every method or class. Remember an attacker only needs to find one way in. Even if just a single access control check is "missed", the confidentiality and/or integrity of a resource can be jeopardized. Validating permissions correctly on just the majority of requests is insufficient. Specific technologies that can help developers in performing such consistent permission checks include the following:

- [Java/Jakarta EE Filters](https://jakarta.ee/specifications/platform/8/apidocs/javax/servlet/Filter.html) including implementations in [Spring Security](https://docs.spring.io/spring-security/site/docs/5.4.0/reference/html5/#servlet-security-filters)
- [Middleware in the Django Framework](https://docs.djangoproject.com/en/4.0/ref/middleware/)
- [.NET Core Filters](https://docs.microsoft.com/en-us/aspnet/core/mvc/controllers/filters?view=aspnetcore-3.1#authorization-filters)
- [Middleware in the Laravel PHP Framework](https://laravel.com/docs/8.x/middleware)

### Thoroughly Review the Authorization Logic of Chosen Tools and Technologies, Implementing Custom Logic if Necessary

Today's developers have access to vast amounts of libraries, platforms, and frameworks that allow them to incorporate robust, complex logic into their apps with minimal effort. However, these frameworks and libraries must not be viewed as a quick panacea for all development problems; developers have a duty to use such frameworks responsibly and wisely. Two general concerns relevant to framework/library selection as relevant to proper access control are misconfiguration/lack of configuration on the part of the developer and vulnerabilities within the components themselves (see [A6](https://owasp.org/www-project-top-ten/OWASP_Top_Ten_2017/Top_10-2017_A6-Security_Misconfiguration) and [A9](https://owasp.org/www-project-top-ten/2017/A9_2017-Using_Components_with_Known_Vulnerabilities.html) for general guidance on these topics).

Even in an otherwise securely developed application, vulnerabilities in third-party components can allow an attacker to bypass normal authorization controls. Such concerns need not be restricted to unproven or poorly maintained projects, but affect even the most robust and popular libraries and frameworks. Writing complex, secure software is hard. Even the most competent developers, working on high-quality libraries and frameworks, will make mistakes. Assume any third-party component you incorporate into an application *could* be or become subject to an authorization vulnerability. Important considerations include:

- Create, maintain, and follow processes for detecting and responding to vulnerable components.
- Incorporate tools such as [Dependency Check](https://owasp.org/www-project-dependency-check/) into the SDLC and consider subscribing to data feeds from vendors, [the NVD](https://nvd.nist.gov/vuln/data-feeds), or other relevant sources.
- Implement defense in depth. Do not depend on any single framework, library, technology, or control to be the sole thing enforcing proper access control.

Misconfiguration (or complete lack of configuration) is another major area in which the components developers build upon can lead to broken authorization.  These components are typically intended to be relatively general purpose tools made to appeal to a wide audience. For all but the simplest use cases, these frameworks and libraries must be customized or supplemented with additional logic in order to meet the unique requirements of a particular app or environment. This consideration is especially important when security requirements, including authorization, are concerned. Notable configuration considerations for authorization include the following:

- Take time to thoroughly understand any technology you build authorization logic upon. Analyze the technology's capabilities with an understanding that *the authorization logic provided by the component may be insufficient for your application's specific security requirements*. Relying on prebuilt logic may be convenient, but this does not mean it is sufficient. Understand that custom authorization logic may well be necessary to meet an app's security requirements.
- Do not let the capabilities of any library, platform, or framework guide your authorization requirements. Rather, authorization requirements should be decided first and then the third-party components may be analyzed in light of these requirements.
- Do not rely on default configurations.
- Test configuration. Do not just assume any configuration performed on a third-party component will work exactly as intended in your particular environment. Documentation can be misunderstood, vague, outdated, or simply inaccurate.

### Prefer Attribute and Relationship Based Access Control over RBAC

In software engineering, two basic forms of access control are widely utilized: Role-Based Access Control (RBAC) and Attribute-Based Access Control (ABAC). There is a third, more recent, model which has gained popularity: Relationship-Based Access Control (ReBAC). The decision between the models has significant implications for the entire SDLC and should be made as early as possible.

- RBAC is a model of access control in which access is granted or denied based upon the roles assigned to a user. Permissions are not directly assigned to an entity; rather, permissions are associated with a role and the entity inherits the permissions of any roles assigned to it. Generally, the relationship between roles and users can be many-to-many, and roles may be hierarchical in nature.

- ABAC may be defined as an access control model where "subject requests to perform operations on objects are granted or denied based on assigned attributes of the subject, assigned attributes of the object, environment conditions, and a set of policies that are specified in terms of those attributes and conditions" ([NIST SP 800-162](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-162.pdf), pg. 7). As defined in NIST SP 800-162, attributes are simply characteristics that can be represented as name-value pairs and assigned to a subject, object, or the environment. Job role, time of day, project name, MAC address, and creation date are but a very small sampling of possible attributes that highlight the flexibility of ABAC implementations.

- ReBAC is an access control model that grants access based on the relationships between resources. For instance, allowing only the user who created a post to edit it. This is especially necessary in social network applications, like Twitter or Facebook, where users want to limit access to their data (tweets or posts) to people they choose (friends, family, followers).

Although RBAC has a long history and remains popular among software developers today, ABAC and ReBAC should typically be preferred for application development. Their advantages over RBAC include:

- **Support fine-grained, complex Boolean logic**. In RBAC, access decisions are made on the presence or absence of roles; that is, the main characteristic of a requesting entity considered is the role(s) assigned to it. Such simplistic logic does a poor job of supporting object-level or horizontal access control decisions and those that require multiple factors.

    - ABAC greatly expands both the number and type of characteristics that can be considered. In ABAC, a "role" or job function can certainly be one attribute assigned to a subject, but it need not be considered in isolation (or at all if this characteristic is not relevant to the particular access requested). Furthermore, ABAC can incorporate environmental and other dynamic attributes, such as time of day, type of device used, and geographic location. Denying access to a sensitive resource outside of normal business hours or if a user has not recently completed mandatory training are just a couple of examples where ABAC could meet access control requirements that RBAC would struggle to fulfill. Thus, ABAC is more effective than RBAC in addressing the principle of least privileges.
    - ReBAC, since it supports assigning relationships between direct objects and direct users (and not just a role), allows for fine-grained permissions. Some systems also support algebraic operators like AND and NOT to express policies like "if this user has relationship X but not relationship Y with the object, then grant access".

- **Robustness**. In large projects or when numerous roles are present, it is easy to miss or improperly perform role checks ([OWASP C7: Enforce Access Controls](https://owasp.org/www-project-proactive-controls/v3/en/c7-enforce-access-controls)). This can result in both too much and too little access. This is especially true in RBAC implementations where a role hierarchy is not present and multiple role checks must be chained to have the desired impact (i.e., `if(user.hasAnyRole("SUPERUSER", "ADMIN", "ACCT_MANAGER"))` ).
- **Speed**. In RBAC, "role explosion" can occur when a system defines too many roles. If users send their credential and roles through means like HTTP headers, which have size limits, there may not be enough space to include all of the user's roles. A viable workaround to this problem is to only send the user ID, and then the application retrieves the user's roles, but this will increase the latency of every request.
- **Supports Multi-Tenancy and Cross-Organizational Requests**. RBAC is poorly suited for use cases where distinct organizations or customers will need access to the same set of protected resources. Meeting such requirements with RBAC would require highly cumbersome methods such as configuring rule sets for each customer in a multi-tenant environment or requiring pre-provisioning of identities for cross-organizational requests ([OWASP C7](https://owasp.org/www-project-proactive-controls/v3/en/c7-enforce-access-controls); [NIST SP 800-162](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-162.pdf)). By contrast, as long as attributes are consistently defined, ABAC implementations allow access control decisions to be "executed and administered in the same or separate infrastructures, while maintaining appropriate levels of security" ([NIST SP 800-162](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-162.pdf), pg. 6).
- **Ease of Management**. Although the initial setup for RBAC is often simpler than ABAC, this short-term benefit quickly vanishes as the scale and complexity of a system grows. In the beginning, a couple of simple roles, such as User and Admin, may suffice for some apps, but this is very unlikely to hold true for any length of time in production applications. As roles become more numerous, both testing and auditing, critical processes for establishing trust in one's codebase and logic, become more difficult ([OWASP C7](https://owasp.org/www-project-proactive-controls/v3/en/c7-enforce-access-controls)). By contrast, ABAC and ReBAC are far more expressive, incorporate attributes and Boolean logic that better reflects real-world concerns, are easier to update when access-control needs change, and encourages the separation of policy management from  enforcement and provisioning of identities ([NIST SP 800-162](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-162.pdf); see also [XACML-V3.0](https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.html) for a standard that highlights these benefits)

### Ensure Lookup IDs are Not Accessible Even When Guessed or Cannot Be Tampered With

Applications often expose the internal object identifiers (such as an account number or Primary Key in a database) that are used to locate and reference an object. This ID may be exposed as a query parameter, path variable, "hidden" form field or elsewhere. For example:

```https://mybank.com/accountTransactions?acct_id=901```

Based on this URL, one could reasonably assume that the application will return a listing of transactions and that the transactions returned will be restricted to a particular account - the account indicated in the `acct_id` param. But what would happen if the user changed the value of the `acct_id` param to another value such as `523`. Will the user be able to view transactions associated with another account even if it does not belong to them? If not, will the failure simply be the result of the account "523" not existing/not being found or will it be due to a failed access control check? Although this example may be an oversimplification, it illustrates a very common security flaw in application development - [CWE 639: Authorization Bypass Through User-Controlled Key](https://cwe.mitre.org/data/definitions/639.html).  When exploited, this weakness can result in authorization bypasses, horizontal privilege escalation and, less commonly, vertical privilege escalation (see [CWE-639](https://cwe.mitre.org/data/definitions/639.html)). This type of vulnerability also represents a form of Insecure Direct Object Reference (IDOR). The following paragraphs will describe the weakness and possible mitigations.

 In the example above, the lookup ID was not only exposed to the user and readily tampered with, but also appears to have been a fairly predictable, perhaps sequential, value.  While one can use various techniques to mask or randomize these IDs and make them hard to guess, such an approach is generally not sufficient by itself. A user should not be able to access a resource they do not have permissions simply because they are able to guess and manipulate that object's identifier in a query param or elsewhere. Rather than relying on some form of security through obscurity, the focus should be on controlling access to the underlying objects and/or the identifiers themselves. Recommended mitigations for this weakness include the following:

- Avoid exposing identifiers to the user when possible. For example it should be possible to retrieve some objects, such as account details,  based solely on currently authenticated user's identity and attributes (e.g. through information contained in a securely implemented JSON Web Token (JWT) or server-side session).
- Implement user/session specific indirect references using a tool such as [OWASP ESAPI](https://owasp.org/www-project-enterprise-security-api/) (see [OWASP Top 10:2025 A01 Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) and the [Insecure Direct Object Reference Prevention Cheat Sheet](Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.md))
- Perform access control checks on *every* request for the *specific* object or functionality being accessed. Just because a user has access to an object of a particular type does not mean they should have access to every object of that particular type.

### Enforce Authorization Checks on Static Resources

The importance of securing static resources is often overlooked or at least overshadowed by other security concerns. Although securing databases and similar data stores often justly receive significant attention from security conscious teams, static resources must also be appropriately secured. Although unprotected static resources are certainly a problem for websites and web applications of all forms, in recent years, poorly secured resources in cloud storage offerings (such as Amazon S3 Buckets) have risen to prominence. When securing static resources, consider the following:

- Ensure that static resources are incorporated into access control policies. The type of protection required for static resources will necessarily be highly contextual. It may be perfectly acceptable for some static resources to be publicly accessible, while others should only be accessible when a highly restrictive set of user and environmental attributes are present. Understanding the type of data exposed in the specific resources under consideration is thus critical. Consider whether a formal Data Classification scheme should be established and incorporated into the application's access control logic (see [here](https://resources.infosecinstitute.com/information-and-asset-classification/) for an overview of data classification).
- Ensure any cloud-based services used to store static resources are secured using the configuration options and tools provided by the vendor. Review the cloud provider's documentation (see guidance from [AWS](https://aws.amazon.com/premiumsupport/knowledge-center/secure-s3-resources/), [Google Cloud](https://cloud.google.com/storage/docs/best-practices#security) and [Azure](https://docs.microsoft.com/en-us/azure/storage/blobs/security-recommendations) for specific implementation details).
- When possible, protect static resources using the same access control logic and mechanisms that are used to secure other application resources and functionality.

### Verify that Authorization Checks are Performed in the Right Location

Developers must never rely on client-side access control checks. While such checks may be permissible for improving the user experience, they should never be the decisive factor in granting or denying access to a resource; client-side logic is often easy to bypass. Access control checks must be performed server-side, at the gateway, or using serverless functions (see [OWASP ASVS 4.0.3, V1.4.1 and V4.1.1](https://raw.githubusercontent.com/OWASP/ASVS/v4.0.3/4.0/OWASP%20Application%20Security%20Verification%20Standard%204.0.3-en.pdf))

### Exit Safely when Authorization Checks Fail

Failed access control checks are a normal occurrence in a secured application; consequently, developers must plan for such failures and handle them securely. Improper handling of such failures can lead to the application being left in an unpredictable state ([CWE-280: Improper Handling of Insufficient Permissions or Privileges](https://cwe.mitre.org/data/definitions/280.html)). Specific recommendations include the following:

- Ensure all exception and failed access control checks are handled no matter how unlikely they seem ([OWASP Top Ten Proactive Controls C10: Handle all errors and exceptions](https://owasp.org/www-project-proactive-controls/v3/en/c10-errors-exceptions)). This does not mean that an application should always try to "correct" for a failed check; oftentimes a simple message or HTTP status code is all that is required.
- Centralize the logic for handling failed access control checks.
- Verify the handling of exceptions and authorization failures. Ensure that such failures, no matter how unlikely, do not put the software into an unstable state that could lead to authorization bypass.
- Ensure sensitive information, such as system logs or debugging output, is not exposed in error messages. Misconfigured error messages can increase the attack surface of your application. ([CWE-209: Generation of Error Message Containing Sensitive Information](https://cwe.mitre.org/data/definitions/209.html))

### Implement Appropriate Logging

Logging is one of the most important detective controls in application security; insufficient logging and monitoring is recognized as among  the most critical security risks in [OWASP's Top Ten 2021](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/). Appropriate logs can not only detect malicious activity, but are also invaluable resources in post-incident investigations, can be used to troubleshoot access control and other security related problems, and are useful in security auditing. Though easy to overlook during the initial design and requirements phase, logging is an important component of holistic application security and must be incorporated into all phases of the SDLC. Recommendations for logging include the following:

- Log using consistent, well-defined formats that can be readily parsed for analysis. According to [OWASP Top Ten Proactive Controls C9](https://owasp.org/www-project-proactive-controls/v3/en/c9-security-logging), [Apache Logging Services](https://logging.apache.org/) is one example of a project that provides support for numerous languages and platforms
- Carefully determine the amount of information to log. This should be determined according to the specific application environment and requirements. Both too much and too little logging may be considered security weaknesses (see [CWE-778](https://cwe.mitre.org/data/definitions/778.html) and [CWE-779](https://cwe.mitre.org/data/definitions/779.html)). Too little logging can result in malicious activity going undetected and greatly reduce the effectiveness of post-incident analysis. Too much logging not only can strain resources and lead to excessive false positives, but may also result in sensitive data being needlessly logged.
- Ensure clocks and timezones are synchronized across systems. Accuracy is crucial in piecing together the sequence of an attack during and after incident response.
- Consider incorporating application logs into a centralized log server or SIEM.

### Create Unit and Integration Test Cases for Authorization Logic

Unit and integration testing are essential for verifying that an application performs as expected and consistently across changes. Flaws in access control logic can be subtle, particularly when requirements are complex; however, even a small logical or configuration error in access control can result in severe consequences. Although not a substitution for a dedicated security test or penetration test (see [OWASP WSTG 4.5](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/05-Authorization_Testing/README) for an excellent guide on this topic as it relates to access control), automated unit and integration testing of access control logic can help reduce the number of security flaws that make it into production. These tests are good at catching the "low-hanging fruit" of security issues but not more sophisticated attack vectors ([OWASP SAMM: Security Testing](https://owaspsamm.org/model/verification/security-testing/)).

Unit and integration testing should aim to incorporate many of the concepts explored in this document. For example, is access being denied by default? Does the application terminate safely when an access control check fails, even under abnormal conditions? Are ABAC policies being properly enforced? While simple unit and integration tests can never replace manual testing performed by a skilled hacker, they are an important tool for detecting and correcting security issues quickly and with far less resources than manual testing.

## References

- [NIST SP 800-162: Guide to Attribute Based Access Control (ABAC) Definition and Considerations](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-162.pdf)
- [OWASP Proactive Controls 2018: Enforce Access Controls](https://top10proactive.owasp.org/archive/2018/c7-enforce-access-controls/)
- [Ferraiolo and Kuhn: Role-Based Access Controls (1992)](https://csrc.nist.gov/files/pubs/conference/1992/10/13/rolebased-access-controls/final/docs/ferraiolo-kuhn-92.pdf)

---

## Section 14: Input Validation Cheat Sheet

# Input Validation Cheat Sheet

## Introduction

Input validation checks whether data meets an application's requirements before the application uses it. It reduces the risk of malformed data, invalid business operations, and excessive resource consumption. [OWASP's Proactive Control C3](https://top10proactive.owasp.org/archive/2024/the-top-10/c3-validate-input-and-handle-exceptions/) distinguishes validation from the additional defenses needed when using that data:

- Use [parameterized queries](SQL_Injection_Prevention_Cheat_Sheet.md) for SQL and [context-aware output encoding](Cross_Site_Scripting_Prevention_Cheat_Sheet.md#output-encoding) to prevent cross-site scripting (XSS).
- Check [authorization](Authorization_Cheat_Sheet.md) separately: a valid account identifier does not mean the caller may access that account.

## Input Validation Strategies

Validate both **syntax** (the expected type and format) and **semantics** (whether the value makes sense for the operation). For example, a booking needs valid dates and an end date after its start date. [CWE-20](https://cwe.mitre.org/data/definitions/20.html) describes these checks, including consistency between related fields.

Define rules for each field:

| Input | Rules to enforce |
| --- | --- |
| Fixed choices | Exact membership in the allowed set, including values submitted from drop-down menus |
| Numbers and dates | Expected type, accepted format, and minimum and maximum values |
| Strings | Length limits and the characters or structure required by the field |
| Objects | Allowed fields, required fields, and rules for missing or null values |
| Arrays | Minimum and maximum item counts and validation of every item, including nested objects |

### Allowlist vs Denylist

Define what the application accepts and reject values outside those rules. Do not try to recognize every malicious string. Blocking apostrophes, for example, rejects legitimate names without making a database query safe. For free-form comments, an allowlist can permit broad Unicode text while limiting its length; it need not restrict users to letters and digits.

## Implementing Input Validation

### Parse Safely, Then Validate

Apply request size limits before buffering or parsing input, and configure parser limits such as maximum nesting depth. JSON explicitly supports [implementation limits on size, depth, and numbers](https://www.rfc-editor.org/info/rfc8259/#section-9). A schema check after parsing cannot protect a parser that has already exhausted resources.

Use a maintained parser for the expected format, handle parsing failures, and validate the resulting values before business processing or storage. Configure parsers for untrusted input; see [XML External Entity Prevention](XML_External_Entity_Prevention_Cheat_Sheet.md#general-guidance) and [Deserialization](Deserialization_Cheat_Sheet.md). Converting text to an integer only establishes a type: it does not establish an acceptable quantity.

Decode according to the protocol before checking field rules. Validate the representation that will actually be used, and avoid decoding it again downstream; [CWE-20](https://cwe.mitre.org/data/definitions/20.html) explains how inconsistent decoding can invalidate earlier checks.

### Validate Structured Data

Use your framework's validators or a schema validator to enforce field rules. For JSON, explicitly configure [required and additional properties](https://json-schema.org/understanding-json-schema/reference/object); listing a property alone neither requires it nor rejects unknown fields. Apply schemas to nested objects and use [item schemas and array length limits](https://json-schema.org/understanding-json-schema/reference/array). Keep business checks, such as date ordering, alongside these structural checks.

Reject invalid requests with a clear error; do not continue with partially validated data. Bind only intended input fields to application objects; see [Mass Assignment](Mass_Assignment_Cheat_Sheet.md).

### Validating Free-form Unicode Text

Agree on a character encoding across components and reject malformed input. Preserve legitimate punctuation and scripts in names and comments. Where a field requires Unicode normalization for consistent comparison, define and apply the same policy before validation, storage, and comparison. [Unicode Standard Annex #15](https://www.unicode.org/reports/tr15/) defines the normalization forms and warns that compatibility normalization can erase meaningful distinctions. Normalization is not sanitization and does not replace output encoding.

### Regular Expressions (Regex)

Use regular expressions for simple, structured fields. Require a match of the entire value, using an API such as [Python's `fullmatch`](https://docs.python.org/3/library/re.html#re.fullmatch) where available. Check the engine's character classes and newline behavior rather than assuming patterns behave identically across languages.

Bound input length before matching, avoid patterns with excessive backtracking, and use a non-backtracking engine or a match timeout where supported. Test valid, invalid, and near-matching values; [Microsoft's regex guidance](https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-regex) explains why near-matches can cause denial of service. Treat a timeout as validation failure.

### Validating Rich User Content

When accepting user-authored HTML, use a maintained [HTML sanitization library](Cross_Site_Scripting_Prevention_Cheat_Sheet.md#html-sanitization). Input validation and regular expressions cannot replace that control.

### File Upload Validation

Treat the submitted filename and content type as untrusted metadata. Validate filenames after protocol decoding; an allowed extension alone does not establish safe content. Follow the [File Upload Cheat Sheet](File_Upload_Cheat_Sheet.md) for content checks, size limits, storage, and safe serving.

### Email Address Validation

Use a maintained email validation library compatible with the addresses your mail system supports. Format validation does not prove mailbox access. Follow [Email Validation and Verification](Email_Validation_and_Verification_Cheat_Sheet.md) for comparison policies, ownership verification, and email change workflows.

## Common Pitfalls

- **Client-only checks:** Validate on the server even when the browser checks the same fields. [Client-side validation is bypassable](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Form_validation); use it for immediate feedback.
- **Trusting internal sources:** Validate data from internal APIs, partner feeds, queues, and stored records when it crosses a trust boundary. An internal transport does not establish that a value meets the receiving component's rules ([CWE-20](https://cwe.mitre.org/data/definitions/20.html)).
- **Denylisting or “cleaning” input:** Apply field-specific acceptance rules. Removing suspicious characters can change meaning and still does not provide query parameterization or output encoding.
- **Stopping at parsing or outer fields:** Test rejected ranges, missing fields, invalid nested items, and oversized arrays, not just malformed syntax.
- **Assuming regex or Unicode normalization makes data safe:** Check whole-value matching and resource limits; keep normalization consistent with the field's meaning.
- **Trusting upload metadata:** Use the file upload controls above; checking a filename is not checking the file's contents.
- **Logging rejected input verbatim:** Record the failure and relevant metadata without secrets or full request bodies. Escape any retained untrusted values for the log format to prevent log injection; see [Logging: Event collection](Logging_Cheat_Sheet.md#event-collection) and [Data to exclude](Logging_Cheat_Sheet.md#data-to-exclude).

## References

- [OWASP Top 10 Proactive Controls 2024: C3 — Validate all Input & Handle Exceptions](https://top10proactive.owasp.org/archive/2024/the-top-10/c3-validate-input-and-handle-exceptions/)
- [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
- [Unicode Standard Annex #15: Unicode Normalization Forms](https://www.unicode.org/reports/tr15/)

---

## Section 15: Java Security Cheat Sheet

# Java Security Cheat Sheet

## Injection Prevention in Java

This section aims to provide tips to handle *Injection* in Java application code.

Sample code used in tips is located [here](https://github.com/righettod/injection-cheat-sheets).

### What is Injection

[Injection](https://owasp.org/www-project-top-ten/OWASP_Top_Ten_2017/Top_10-2017_A1-Injection) in OWASP Top 10 is defined as following:

*Consider anyone who can send untrusted data to the system, including external users, internal users, and administrators.*

### General advice to prevent Injection

The following point can be applied, in a general way, to prevent *Injection* issue:

1. Apply **Input Validation** (using allowlist approach) combined with **Output Sanitizing+Escaping** on user input/output.
2. If you need to interact with system, try to use API features provided by your technology stack (Java / .Net / PHP...) instead of building command.

Additional advice is provided on this [cheatsheet](Input_Validation_Cheat_Sheet.md).

## Specific Injection types

*Examples in this section will be provided in Java technology (see Maven project associated) but advice is applicable to others technologies like .Net / PHP / Ruby / Python...*

### SQL

#### Symptom

Injection of this type occur when the application uses untrusted user input to build an SQL query using a String and execute it.

#### How to prevent

Use *Query Parameterization* in order to prevent injection.

#### Example

``` java
/*No DB framework used here in order to show the real use of
  Prepared Statement from Java API*/
/*Open connection with H2 database and use it*/
Class.forName("org.h2.Driver");
String jdbcUrl = "jdbc:h2:file:" + new File(".").getAbsolutePath() + "/target/db";
try (Connection con = DriverManager.getConnection(jdbcUrl)) {

    /* Sample A: Select data using Prepared Statement*/
    String query = "select * from color where friendly_name = ?";
    List<String> colors = new ArrayList<>();
    try (PreparedStatement pStatement = con.prepareStatement(query)) {
        pStatement.setString(1, "yellow");
        try (ResultSet rSet = pStatement.executeQuery()) {
            while (rSet.next()) {
                colors.add(rSet.getString(1));
            }
        }
    }

    /* Sample B: Insert data using Prepared Statement*/
    query = "insert into color(friendly_name, red, green, blue) values(?, ?, ?, ?)";
    int insertedRecordCount;
    try (PreparedStatement pStatement = con.prepareStatement(query)) {
        pStatement.setString(1, "orange");
        pStatement.setInt(2, 239);
        pStatement.setInt(3, 125);
        pStatement.setInt(4, 11);
        insertedRecordCount = pStatement.executeUpdate();
    }

   /* Sample C: Update data using Prepared Statement*/
    query = "update color set blue = ? where friendly_name = ?";
    int updatedRecordCount;
    try (PreparedStatement pStatement = con.prepareStatement(query)) {
        pStatement.setInt(1, 10);
        pStatement.setString(2, "orange");
        updatedRecordCount = pStatement.executeUpdate();
    }

   /* Sample D: Delete data using Prepared Statement*/
    query = "delete from color where friendly_name = ?";
    int deletedRecordCount;
    try (PreparedStatement pStatement = con.prepareStatement(query)) {
        pStatement.setString(1, "orange");
        deletedRecordCount = pStatement.executeUpdate();
    }

}
```

#### References

- [SQL Injection Prevention Cheat Sheet](SQL_Injection_Prevention_Cheat_Sheet.md)

### JPA

#### Symptom

Injection of this type occur when the application uses untrusted user input to build a JPA query using a String and execute it. It's quite similar to SQL injection but here the altered language is not SQL but JPA QL.

#### How to prevent

Use Java Persistence Query Language **Query Parameterization** in order to prevent injection.

#### Example

``` java
EntityManager entityManager = null;
try {
    /* Get a ref on EntityManager to access DB */
    entityManager = Persistence.createEntityManagerFactory("testJPA").createEntityManager();

    /* Define parameterized query prototype using named parameter to enhance readability */
    String queryPrototype = "select c from Color c where c.friendlyName = :colorName";

    /* Create the query, set the named parameter and execute the query */
    Query queryObject = entityManager.createQuery(queryPrototype);
    Color c = (Color) queryObject.setParameter("colorName", "yellow").getSingleResult();

} finally {
    if (entityManager != null && entityManager.isOpen()) {
        entityManager.close();
    }
}
```

#### References

- [SQLi and JPA](https://software-security.sans.org/developer-how-to/fix-sql-injection-in-java-persistence-api-jpa)

### Operating System

#### Symptom

Injection of this type occur when the application uses untrusted user input to build an Operating System command using a String and execute it.

#### How to prevent

Use technology stack **API** in order to prevent injection.

#### Example

``` java
/* The context taken is, for example, to perform a PING against a computer.
* The prevention is to use the feature provided by the Java API instead of building
* a system command as String and execute it */
InetAddress host = InetAddress.getByName("localhost");
var reachable = host.isReachable(5000);
```

#### References

- [Command Injection](https://owasp.org/www-community/attacks/Command_Injection)

### XML: XPath Injection

#### Symptom

Injection of this type occur when the application uses untrusted user input to build a XPath query using a String and execute it.

#### How to prevent

Use **XPath Variable Resolver** in order to prevent injection.

#### Example

**Variable Resolver** implementation.

``` java
/**
 * Resolver in order to define parameter for XPATH expression.
 *
 */
public class SimpleVariableResolver implements XPathVariableResolver {

    private final Map<QName, Object> vars = new HashMap<QName, Object>();

    /**
     * External methods to add parameter
     *
     * @param name Parameter name
     * @param value Parameter value
     */
    public void addVariable(QName name, Object value) {
        vars.put(name, value);
    }

    /**
     * {@inheritDoc}
     *
     * @see javax.xml.xpath.XPathVariableResolver#resolveVariable(javax.xml.namespace.QName)
     */
    public Object resolveVariable(QName variableName) {
        return vars.get(variableName);
    }
}
```

Code using it to perform XPath query.

``` java
/*Create a XML document builder factory*/
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();

/*Disable External Entity resolution for different cases*/
//Do not performed here in order to focus on variable resolver code
//but do it for production code !

/*Load XML file*/
DocumentBuilder builder = dbf.newDocumentBuilder();
Document doc = builder.parse(new File("src/test/resources/SampleXPath.xml"));

/* Create and configure parameter resolver */
String bid = "bk102";
SimpleVariableResolver variableResolver = new SimpleVariableResolver();
variableResolver.addVariable(new QName("bookId"), bid);

/*Create and configure XPATH expression*/
XPath xpath = XPathFactory.newInstance().newXPath();
xpath.setXPathVariableResolver(variableResolver);
XPathExpression xPathExpression = xpath.compile("//book[@id=$bookId]");

/* Apply expression on XML document */
Object nodes = xPathExpression.evaluate(doc, XPathConstants.NODESET);
NodeList nodesList = (NodeList) nodes;
Element book = (Element)nodesList.item(0);
var containsRalls = book.getTextContent().contains("Ralls, Kim");
```

#### References

- [XPATH Injection](https://owasp.org/www-community/attacks/XPATH_Injection)

### HTML/JavaScript/CSS

#### Symptom

Injection of this type occur when the application uses untrusted user input to build an HTTP response and sent it to browser.

#### How to prevent

Use [context-specific output encoding](https://owasp.org/projects/java-encoder?tab=how-to-use) when displaying untrusted text. When the application intentionally accepts HTML markup, use an [HTML sanitization policy](https://github.com/OWASP/java-html-sanitizer#crafting-a-policy) for the permitted elements and attributes. Input validation enforces business rules; it does not replace these XSS controls. See the [XSS Prevention Cheat Sheet](Cross_Site_Scripting_Prevention_Cheat_Sheet.md) for HTML, attribute, JavaScript, and CSS context requirements.

#### Example

``` java
// Illustrative business validation; output still needs the appropriate XSS control.
String userInput = "You user login is owasp-user01";

/* First we check that the value contains only expected character*/
if (!Pattern.matches("[a-zA-Z0-9\\s\\-]{1,50}", userInput))
{
    return false;
}

// Plain text for an ordinary HTML body position, such as the content of a div.
String encodedText = Encode.forHtml(userInput);

// Allowed markup for an HTML body position; not for attributes, script, or style.
String outputToUser = "You <p>user login</p> is <strong>owasp-user01</strong>";
outputToUser += "<script>alert(22);</script><img src='#' onload='javascript:alert(23);'>";

/* Create a sanitizing policy that only allow tag '<p>' and '<strong>'*/
PolicyFactory policy = new HtmlPolicyBuilder().allowElements("p", "strong").toFactory();

/* Sanitize the output that will be sent to user*/
String safeOutput = policy.sanitize(outputToUser);

/* Keep the permitted markup: encoding this whole fragment would display tags as text. */
String finalSafeOutputExpected = "You <p>user login</p> is <strong>owasp-user01</strong>";
if (!finalSafeOutputExpected.equals(safeOutput))
{
    return false;
}
```

#### References

- [XSS](https://owasp.org/www-community/attacks/xss/)
- [OWASP Java HTML Sanitizer](https://github.com/owasp/java-html-sanitizer)
- [OWASP Java Encoder](https://github.com/owasp/owasp-java-encoder)
- [Java RegEx](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html)

### LDAP

A dedicated [cheatsheet](LDAP_Injection_Prevention_Cheat_Sheet.md) has been created.

### NoSQL

#### Symptom

Injection of this type occur when the application uses untrusted user input to build a NoSQL API call expression.

#### How to prevent

Validate the expected input type, length, and business format, then use the driver's structured query API. Do not concatenate untrusted values into query strings or accept client-supplied query/operator objects. [MongoDB's driver guidance](https://www.mongodb.com/docs/drivers/client-libraries-best-practices/) distinguishes literal values built through typed APIs from JSON or JavaScript that is parsed as query syntax. A blacklist of punctuation is not needed for the string equality query below. See the [NoSQL Security Cheat Sheet](NoSQL_Security_Cheat_Sheet.md#prevent-nosql-injection) for broader controls.

#### Example - MongoDB

Assume `collection` is an application-configured `MongoCollection<Document>`. This example uses the Java driver's [equality filter builder](https://www.mongodb.com/docs/drivers/java/sync/current/builders/filters/) with a string value; the 50-character limit is an illustrative business rule, not the injection defense.

```java
String userInput = "Brooklyn";
if (userInput == null || userInput.length() > 50) {
    throw new IllegalArgumentException("Invalid borough");
}

// Keep the field name fixed and the input as a string value.
Bson expression = Filters.eq("borough", userInput);
FindIterable<Document> restaurants = collection.find(expression);
```

#### References

- [Testing for NoSQL injection](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05.6-Testing_for_NoSQL_Injection.html)
- [SQL and NoSQL Injection](https://ckarande.gitbooks.io/owasp-nodegoat-tutorial/content/tutorial/a1_-_sql_and_nosql_injection.html)
- [No SQL, No Injection?](https://arxiv.org/ftp/arxiv/papers/1506/1506.04082.pdf)

### Log Injection

#### Symptom

[Log Injection](https://owasp.org/www-community/attacks/Log_Injection) occurs when an application includes untrusted data in an application log message (e.g., an attacker can cause an additional log entry that looks like it came from a completely different user, if they can inject CRLF characters in the untrusted data). More information about this attack is available on the OWASP [Log Injection](https://owasp.org/www-community/attacks/Log_Injection) page.

#### How to prevent

To prevent an attacker from writing malicious content into the application log, apply defenses such as:

- Use structured log formats, such as JSON, instead of unstructured text formats.
  Unstructured formats are susceptible to **C**arriage **R**eturn (CR) and **L**ine **F**eed (LF) injection (see [CWE-93](https://cwe.mitre.org/data/definitions/93.html)).
- Limit the size of the user input value used to create the log message.
- Make sure [all XSS defenses](Cross_Site_Scripting_Prevention_Cheat_Sheet.md) are applied when viewing log files in a web browser.

#### Example using Log4j Core 2

The recommended logging policy for a production environment is sending logs to a network socket using the structured
[JSON Template Layout](https://logging.apache.org/log4j/2.x/manual/json-template-layout.html)
introduced in
[Log4j 2.14.0](https://logging.apache.org/log4j/2.x/release-notes.html#release-notes-2-14-0)
and truncate string values longer than 500 characters using the
[`maxStringLength` configuration attribute](https://logging.apache.org/log4j/2.x/manual/json-template-layout.html#plugin-attr-maxStringLength).
The truncation suffix is appended after this limit; this does not cap the encoded byte size or the total JSON document size:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration xmlns="https://logging.apache.org/xml/ns"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xsi:schemaLocation="
                   https://logging.apache.org/xml/ns
                   https://logging.apache.org/xml/ns/log4j-config-2.xsd">
  <Appenders>
    <Socket name="SOCKET"
            host="localhost"
            port="12345">
      <!-- Truncate strings longer than 500 characters, then append the truncation suffix -->
      <JsonTemplateLayout maxStringLength="500"
                          nullEventDelimiterEnabled="true"/>
    </Socket>
  </Appenders>
  <Loggers>
    <Root level="DEBUG">
      <AppenderRef ref="SOCKET"/>
    </Root>
  </Loggers>
</Configuration>
```

See
[Integration with service-oriented architectures](https://logging.apache.org/log4j/2.x/soa.html)
on
[Log4j website](https://logging.apache.org/log4j/2.x/index.html)
for more tips.

Usage of the logger at code level:

``` java
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
...
// Most common way to declare a logger
private static final Logger logger = LogManager.getLogger();
// GOOD!
//
// Use parameterized logging to add user data to a message
// The pattern should be a compile-time constant
logger.warn("Login failed for user {}.", username);
// BAD!
//
// Don't mix string concatenation and parameters
// If `username` contains `{}`, the exception will leak into the message
logger.warn("Failure for user " + username + " and role {}.", role, ex);
...
```

See
[Log4j API Best Practices](https://logging.apache.org/log4j/2.x/manual/api.html#best-practice)
for more information.

#### Example using Logback

The recommended logging policy for a production environment is using the structured
[JsonEncoder](https://logback.qos.ch/manual/encoders.html#JsonEncoder)
introduced in
[Logback 1.3.8](https://logback.qos.ch/news.html#1.3.8).
In the example below, Logback is configured to roll on 10 log files of 5 MiB each:

``` xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration>
<configuration>
  <import class="ch.qos.logback.classic.encoder.JsonEncoder"/>
  <import class="ch.qos.logback.core.rolling.FixedWindowRollingPolicy"/>
  <import class="ch.qos.logback.core.rolling.RollingFileAppender"/>
  <import class="ch.qos.logback.core.rolling.SizeBasedTriggeringPolicy"/>

  <appender name="RollingFile" class="RollingFileAppender">
    <file>app.log</file>
    <rollingPolicy class="FixedWindowRollingPolicy">
      <fileNamePattern>app-%i.log</fileNamePattern>
      <minIndex>1</minIndex>
      <maxIndex>10</maxIndex>
    </rollingPolicy>
    <triggeringPolicy class="SizeBasedTriggeringPolicy">
      <maxFileSize>5MB</maxFileSize>
    </triggeringPolicy>
    <encoder class="JsonEncoder"/>
  </appender>

  <root level="DEBUG">
    <appender-ref ref="RollingFile"/>
  </root>
</configuration>
```

Usage of the logger at code level:

``` java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
...
// Most common way to declare a logger
Logger logger = LoggerFactory.getLogger(MyClass.class);
// GOOD!
//
// Use parameterized logging to add user data to a message
// The pattern should be a compile-time constant
logger.warn("Login failed for user {}.", username);
// BAD!
//
// Don't mix string concatenation and parameters
// If `username` contains `{}`, the exception will leak into the message
logger.warn("Failure for user " + username + " and role {}.", role, ex);
...
```

#### References

- [Log4j Core Configuration File](https://logging.apache.org/log4j/2.x/manual/configuration.html)
- [Log4j JSON Template Layout](https://logging.apache.org/log4j/2.x/manual/json-template-layout.html)
- [Log4j Appenders](https://logging.apache.org/log4j/2.x/manual/appenders.html)
- [Logback Configuration File](https://logback.qos.ch/manual/configuration.html)
- [Logback JsonEncoder](https://logback.qos.ch/manual/encoders.html#JsonEncoder)
- [Logback Appenders](https://logback.qos.ch/manual/appenders.html)

## Cryptography

### General cryptography guidance

- **Never, ever write your own cryptographic functions.**
- Wherever possible, try and avoid writing any cryptographic code at all. Instead try and either use pre-existing secret management solutions or the secret management solution provided by your cloud provider. For more information, see the [OWASP Secrets Management Cheat Sheet](Secrets_Management_Cheat_Sheet.md).
- If you cannot use a pre-existing secret management solution, try and use a trusted and well known implementation library rather than using the libraries built into JCA/JCE as it is far too easy to make cryptographic errors with them.
- Make sure your application or protocol can easily support a future change of cryptographic algorithms.
- Use your package manager wherever possible to keep all of your packages up to date. Watch the updates on your development setup, and plan updates to your applications accordingly.
- We will show examples below based on Google Tink, which is a library created by cryptography experts for using cryptography safely (in the sense of minimizing common mistakes made when using standard cryptography libraries).

### Encryption for storage

Follow the algorithm guidance in the [OWASP Cryptographic Storage Cheat Sheet](Cryptographic_Storage_Cheat_Sheet.md#algorithms).

#### Symmetric example using Google Tink

Google Tink has documentation on performing common tasks.

For example, this page (from Google's website) shows [how to perform simple symmetric encryption](https://developers.google.com/tink/encrypt-data).

The following code snippet shows an encapsulated use of this functionality:

<details>
  <summary>Click here to view the "Tink symmetric encryption" code snippet.</summary>

``` java
import static java.nio.charset.StandardCharsets.UTF_8;

import com.google.crypto.tink.Aead;
import com.google.crypto.tink.InsecureSecretKeyAccess;
import com.google.crypto.tink.KeysetHandle;
import com.google.crypto.tink.TinkJsonProtoKeysetFormat;
import com.google.crypto.tink.aead.AeadConfig;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;

// AesGcmSimpleTest
public class App {

    // Based on example from:
    // https://github.com/tink-crypto/tink-java/tree/main/examples/aead

    public static void main(String[] args) throws Exception {

        // Key securely generated using:
        // tinkey create-keyset --key-template AES128_GCM --out-format JSON --out aead_test_keyset.json



        // Register all AEAD key types with the Tink runtime.
        AeadConfig.register();

        // Read the keyset into a KeysetHandle.
        KeysetHandle handle =
        TinkJsonProtoKeysetFormat.parseKeyset(
            new String(Files.readAllBytes( Paths.get("/home/fredbloggs/aead_test_keyset.json")), UTF_8), InsecureSecretKeyAccess.get());

        String message = "This message to be encrypted";
        System.out.println(message);

        // Add some relevant context about the encrypted data that should be verified
        // on decryption
        String metadata = "Sender: fredbloggs@example.com";

        // Encrypt the message
        byte[] cipherText = AesGcmSimple.encrypt(message, metadata, handle);
        System.out.println(Base64.getEncoder().encodeToString(cipherText));

        // Decrypt the message
        String message2 = AesGcmSimple.decrypt(cipherText, metadata, handle);
        System.out.println(message2);
    }
}

class AesGcmSimple {

    public static byte[] encrypt(String plaintext, String metadata, KeysetHandle handle) throws Exception {
        // Get the primitive.
        Aead aead = handle.getPrimitive(Aead.class);
        return aead.encrypt(plaintext.getBytes(UTF_8), metadata.getBytes(UTF_8));
    }

    public static String decrypt(byte[] ciphertext, String metadata, KeysetHandle handle) throws Exception {
        // Get the primitive.
        Aead aead = handle.getPrimitive(Aead.class);
        return new String(aead.decrypt(ciphertext, metadata.getBytes(UTF_8)),UTF_8);
    }

}

```

</details>

#### Symmetric example using built-in JCA/JCE classes

If you absolutely cannot use a separate library, it is still possible to use the built JCA/JCE classes but it is strongly recommended to have a cryptography expert review the full design and code, as even the most trivial error can severely weaken your encryption.

The following code snippet shows an example of using AES-GCM to perform encryption/decryption of data.

A few constraints/pitfalls with this code:

- It does not take into account key rotation or management which is a whole topic in itself.
- It is important to use a different nonce for every encryption operation, especially if the same key is used. For more information, see [this answer on Cryptography Stack Exchange](https://crypto.stackexchange.com/a/66500).
- The key will need to be stored securely.

<details>
  <summary>Click here to view the "JCA/JCE symmetric encryption" code snippet.</summary>

```java
import java.nio.charset.StandardCharsets;
import java.security.SecureRandom;
import javax.crypto.spec.*;
import javax.crypto.*;
import java.util.Base64;


// AesGcmSimpleTest
class Main {

    public static void main(String[] args) throws Exception {
        // Key of 32 bytes / 256 bits for AES
        KeyGenerator keyGen = KeyGenerator.getInstance(AesGcmSimple.ALGORITHM);
        keyGen.init(AesGcmSimple.KEY_SIZE, new SecureRandom());
        SecretKey secretKey = keyGen.generateKey();

        // Nonce of 12 bytes / 96 bits and this size should always be used.
        // It is critical for AES-GCM that a unique nonce is used for every cryptographic operation.
        byte[] nonce = new byte[AesGcmSimple.IV_LENGTH];
        SecureRandom random = new SecureRandom();
        random.nextBytes(nonce);

        var message = "This message to be encrypted";
        System.out.println(message);

        // Encrypt the message
        byte[] cipherText = AesGcmSimple.encrypt(message, nonce, secretKey);
        System.out.println(Base64.getEncoder().encodeToString(cipherText));

        // Decrypt the message
        var message2 = AesGcmSimple.decrypt(cipherText, nonce, secretKey);
        System.out.println(message2);
    }
}

class AesGcmSimple {

    public static final String ALGORITHM = "AES";
    public static final String CIPHER_ALGORITHM = "AES/GCM/NoPadding";
    public static final int KEY_SIZE = 256;
    public static final int TAG_LENGTH = 128;
    public static final int IV_LENGTH = 12;

    public static byte[] encrypt(String plaintext, byte[] nonce, SecretKey secretKey) throws Exception {
        return cryptoOperation(plaintext.getBytes(StandardCharsets.UTF_8), nonce, secretKey, Cipher.ENCRYPT_MODE);
    }

    public static String decrypt(byte[] ciphertext, byte[] nonce, SecretKey secretKey) throws Exception {
        return new String(cryptoOperation(ciphertext, nonce, secretKey, Cipher.DECRYPT_MODE), StandardCharsets.UTF_8);
    }

    private static byte[] cryptoOperation(byte[] text, byte[] nonce, SecretKey secretKey, int mode) throws Exception {
        Cipher cipher = Cipher.getInstance(CIPHER_ALGORITHM);
        GCMParameterSpec gcmParameterSpec = new GCMParameterSpec(TAG_LENGTH, nonce);
        cipher.init(mode, secretKey, gcmParameterSpec);
        return cipher.doFinal(text);
    }

}
```

</details>

### Encryption for transmission

Again, follow the algorithm guidance in the [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html#algorithms).

#### Asymmetric example using Google Tink

Google Tink has documentation on performing common tasks.

For example, this page (from Google's website) shows [how to perform a hybrid encryption process](https://developers.google.com/tink/exchange-data) where two parties want to share data based on their asymmetric key pair.

The following code snippet shows how this functionality can be used to share secrets between Alice and Bob:

<details>
  <summary>Click here to view the "Tink hybrid encryption" code snippet.</summary>

``` java
import static java.nio.charset.StandardCharsets.UTF_8;

import com.google.crypto.tink.HybridDecrypt;
import com.google.crypto.tink.HybridEncrypt;
import com.google.crypto.tink.InsecureSecretKeyAccess;
import com.google.crypto.tink.KeysetHandle;
import com.google.crypto.tink.TinkJsonProtoKeysetFormat;
import com.google.crypto.tink.hybrid.HybridConfig;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;

// HybridReplaceTest
class App {
    public static void main(String[] args) throws Exception {
        /*

        Generated public/private keypairs for Bob and Alice using the
        following tinkey commands:

        ./tinkey create-keyset \
        --key-template DHKEM_X25519_HKDF_SHA256_HKDF_SHA256_AES_256_GCM \
        --out-format JSON --out alice_private_keyset.json

        ./tinkey create-keyset \
        --key-template DHKEM_X25519_HKDF_SHA256_HKDF_SHA256_AES_256_GCM \
        --out-format JSON --out bob_private_keyset.json

        ./tinkey create-public-keyset --in alice_private_keyset.json \
        --in-format JSON --out-format JSON --out alice_public_keyset.json

        ./tinkey create-public-keyset --in bob_private_keyset.json \
        --in-format JSON --out-format JSON --out bob_public_keyset.json
        */

        HybridConfig.register();

        // Generate ECC key pair for Alice
        var alice = new HybridSimple(
                getKeysetHandle("/home/alicesmith/private_keyset.json"),
                getKeysetHandle("/home/alicesmith/public_keyset.json")

        );

        KeysetHandle alicePublicKey = alice.getPublicKey();

        // Generate ECC key pair for Bob
        var bob = new HybridSimple(
                getKeysetHandle("/home/bobjones/private_keyset.json"),
                getKeysetHandle("/home/bobjones/public_keyset.json")

        );

        KeysetHandle bobPublicKey = bob.getPublicKey();

        // This keypair generation should be reperformed every so often in order to
        // obtain a new shared secret to avoid a long lived shared secret.

        // Alice encrypts a message to send to Bob
        String plaintext = "Hello, Bob!";

        // Add some relevant context about the encrypted data that should be verified
        // on decryption
        String metadata = "Sender: alicesmith@example.com";

        System.out.println("Secret being sent from Alice to Bob: " + plaintext);
        var cipherText = alice.encrypt(bobPublicKey, plaintext, metadata);
        System.out.println("Ciphertext being sent from Alice to Bob: " + Base64.getEncoder().encodeToString(cipherText));


        // Bob decrypts the message
        var decrypted = bob.decrypt(cipherText, metadata);
        System.out.println("Secret received by Bob from Alice: " + decrypted);
        System.out.println();

        // Bob encrypts a message to send to Alice
        String plaintext2 = "Hello, Alice!";

        // Add some relevant context about the encrypted data that should be verified
        // on decryption
        String metadata2 = "Sender: bobjones@example.com";

        System.out.println("Secret being sent from Bob to Alice: " + plaintext2);
        var cipherText2 = bob.encrypt(alicePublicKey, plaintext2, metadata2);
        System.out.println("Ciphertext being sent from Bob to Alice: " + Base64.getEncoder().encodeToString(cipherText2));

        // Bob decrypts the message
        var decrypted2 = alice.decrypt(cipherText2, metadata2);
        System.out.println("Secret received by Alice from Bob: " + decrypted2);
    }

    private static KeysetHandle getKeysetHandle(String filename) throws Exception
    {
        return TinkJsonProtoKeysetFormat.parseKeyset(
                new String(Files.readAllBytes( Paths.get(filename)), UTF_8), InsecureSecretKeyAccess.get());
    }
}
class HybridSimple {

    private KeysetHandle privateKey;
    private KeysetHandle publicKey;


    public HybridSimple(KeysetHandle privateKeyIn, KeysetHandle publicKeyIn) throws Exception {
        privateKey = privateKeyIn;
        publicKey = publicKeyIn;
    }

    public KeysetHandle getPublicKey() {
        return publicKey;
    }

    public byte[] encrypt(KeysetHandle partnerPublicKey, String message, String metadata) throws Exception {

        HybridEncrypt encryptor = partnerPublicKey.getPrimitive(HybridEncrypt.class);

        // return the encrypted value
        return encryptor.encrypt(message.getBytes(UTF_8), metadata.getBytes(UTF_8));
    }
    public String decrypt(byte[] ciphertext, String metadata) throws Exception {

        HybridDecrypt decryptor = privateKey.getPrimitive(HybridDecrypt.class);

        // return the encrypted value
        return new String(decryptor.decrypt(ciphertext, metadata.getBytes(UTF_8)),UTF_8);
    }


}
```

</details>

#### Asymmetric example using built-in JCA/JCE classes

If you absolutely cannot use a separate library, it is still possible to use the built JCA/JCE classes but it is strongly recommended to have a cryptography expert review the full design and code, as even the most trivial error can severely weaken your encryption.

This Java 25+ example illustrates Elliptic Curve Diffie-Hellman (ECDH) followed by HKDF-SHA-256 and AES-GCM. Do not use raw ECDH output directly as an AES key: [RFC 5869](https://www.rfc-editor.org/rfc/rfc5869.html#section-3.3) explains why Diffie-Hellman values need extraction. The [Java KDF API](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/javax/crypto/KDF.html) performs both extraction and expansion here. This is a primitive demonstration, not an authenticated communication protocol.

Note that this code sample relies on the AesGcmSimple class from the [previous section](#symmetric-example-using-built-in-jcajce-classes).

A few constraints/pitfalls with this code:

- It does not take into account key rotation or management which is a whole topic in itself.
- The code deliberately enforces a new nonce for every encryption operation but this must be managed as a separate data item alongside the ciphertext.
- The private keys will need to be stored securely.
- The code does not consider the validation of public keys before use.
- Public keys must be authenticated independently before use. HKDF does not authenticate the peer; this example omits that protocol and its identity/context binding.

<details>
  <summary>Click here to view the "JCA/JCE hybrid encryption" code snippet.</summary>

```java
import java.nio.charset.StandardCharsets;
import java.security.SecureRandom;
import javax.crypto.spec.*;
import javax.crypto.*;
import java.util.*;
import java.security.*;
import java.security.spec.*;
import java.util.Arrays;

// ECDHSimpleTest
class Main {
    public static void main(String[] args) throws Exception {

        // Generate ECC key pair for Alice
        var alice = new ECDHSimple();
        Key alicePublicKey = alice.getPublicKey();

        // Generate ECC key pair for Bob
        var bob = new ECDHSimple();
        Key bobPublicKey = bob.getPublicKey();

        // This keypair generation should be reperformed every so often in order to
        // obtain a new shared secret to avoid a long lived shared secret.

        // Alice encrypts a message to send to Bob
        String plaintext = "Hello"; //, Bob!";
        System.out.println("Secret being sent from Alice to Bob: " + plaintext);

        var retPair = alice.encrypt(bobPublicKey, plaintext);
        var nonce = retPair.getKey();
        var cipherText = retPair.getValue();

        System.out.println("Both cipherText and nonce being sent from Alice to Bob: " + Base64.getEncoder().encodeToString(cipherText) + " " + Base64.getEncoder().encodeToString(nonce));


        // Bob decrypts the message
        var decrypted = bob.decrypt(alicePublicKey, cipherText, nonce);
        System.out.println("Secret received by Bob from Alice: " + decrypted);
        System.out.println();

        // Bob encrypts a message to send to Alice
        String plaintext2 = "Hello"; //, Alice!";
        System.out.println("Secret being sent from Bob to Alice: " + plaintext2);

        var retPair2 = bob.encrypt(alicePublicKey, plaintext2);
        var nonce2 = retPair2.getKey();
        var cipherText2 = retPair2.getValue();
        System.out.println("Both cipherText2 and nonce2 being sent from Bob to Alice: " + Base64.getEncoder().encodeToString(cipherText2) + " " + Base64.getEncoder().encodeToString(nonce2));

        // Bob decrypts the message
        var decrypted2 = alice.decrypt(bobPublicKey, cipherText2, nonce2);
        System.out.println("Secret received by Alice from Bob: " + decrypted2);
    }
}
class ECDHSimple {
    private KeyPair keyPair;

    public class AesKeyNonce {
        public SecretKey Key;
        public byte[] Nonce;
    }

    public ECDHSimple() throws Exception {
        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("EC");
        ECGenParameterSpec ecSpec = new ECGenParameterSpec("secp256r1"); // Using secp256r1 curve
        keyPairGenerator.initialize(ecSpec);
        keyPair = keyPairGenerator.generateKeyPair();
    }

    public Key getPublicKey() {
        return keyPair.getPublic();
    }

    public AbstractMap.SimpleEntry<byte[], byte[]> encrypt(Key partnerPublicKey, String message) throws Exception {

        // Generate the AES Key and Nonce
        AesKeyNonce aesParams = generateAESParams(partnerPublicKey);

        // return the encrypted value
        return new AbstractMap.SimpleEntry<>(
            aesParams.Nonce,
            AesGcmSimple.encrypt(message, aesParams.Nonce, aesParams.Key)
            );
    }
    public String decrypt(Key partnerPublicKey, byte[] ciphertext, byte[] nonce) throws Exception {

        // Generate the AES Key and Nonce
        AesKeyNonce aesParams = generateAESParams(partnerPublicKey, nonce);

        // return the decrypted value
        return AesGcmSimple.decrypt(ciphertext, aesParams.Nonce, aesParams.Key);
    }

    private AesKeyNonce generateAESParams(Key partnerPublicKey, byte[] nonce) throws Exception {

        // Derive the secret based on this side's private key and the other side's public key
        KeyAgreement keyAgreement = KeyAgreement.getInstance("ECDH");
        keyAgreement.init(keyPair.getPrivate());
        keyAgreement.doPhase(partnerPublicKey, true);
        byte[] secret = keyAgreement.generateSecret();

        AesKeyNonce aesKeyNonce = new AesKeyNonce();

        // Illustrative domain label; a real protocol defines its full context binding.
        byte[] info = "OWASP Java ECDH example: AES-256-GCM v1".getBytes(StandardCharsets.UTF_8);
        var derivation = HKDFParameterSpec.ofExtract().addIKM(secret)
                .thenExpand(info, AesGcmSimple.KEY_SIZE / 8);
        aesKeyNonce.Key = KDF.getInstance("HKDF-SHA256").deriveKey("AES", derivation);
        Arrays.fill(secret, (byte) 0);

        // Passed in nonce will be used.
        aesKeyNonce.Nonce = nonce;
        return aesKeyNonce;

    }

    private AesKeyNonce generateAESParams(Key partnerPublicKey) throws Exception {

        // Nonce of 12 bytes / 96 bits and this size should always be used.
        // It is critical for AES-GCM that a unique nonce is used for every cryptographic operation.
        // Therefore this is not generated from the shared secret
        byte[] nonce = new byte[AesGcmSimple.IV_LENGTH];
        SecureRandom random = new SecureRandom();
        random.nextBytes(nonce);
        return generateAESParams(partnerPublicKey, nonce);

    }
}
```

</details>

## References

- [Oracle: Secure Coding Guidelines for Java SE](https://www.oracle.com/java/technologies/javase/seccodeguide.html)
- [Tink: Authenticated Encryption with Associated Data](https://developers.google.com/tink/aead)

---

## Section 16: Secrets Management Cheat Sheet

# Secrets Management Cheat Sheet

## 1 Introduction

Secrets are being used everywhere nowadays, especially with the popularity of the DevOps movement. Application Programming Interface (API) keys, database credentials, Identity and Access Management (IAM) permissions, Secure Shell (SSH) keys, certificates, etc. Many organizations have them hardcoded within the source code in plaintext, littered throughout configuration files and configuration management tools.

There is a growing need for organizations to centralize the storage, provisioning, auditing, rotation and management of secrets to control access to secrets and prevent them from leaking and compromising the organization. Often, services share the same secrets, which makes identifying the source of compromise or leak challenging.

This cheat sheet offers best practices and guidelines to help properly implement secrets management.

## 2 General Secrets Management

The following sections address the main concepts relating to secrets management.

### 2.1 High Availability

It is vital to select a technology that is robust enough to service traffic reliably:

- Users (e.g., SSH keys, root account passwords). In an incident response scenario, users expect to be provisioned with credentials rapidly, so they can recover services that have gone offline. Having to wait for credentials could impact the responsiveness of the operations team.
- Applications (e.g., database credentials and API keys). If the service is not performant, it could degrade the availability of dependent applications or increase application startup times.

Such a service could receive a considerable volume of requests within a large organization.

### 2.2 Centralize and Standardize

Secrets used by your DevOps teams for your applications might be consumed differently than secrets stored by your marketeers or your SRE team. You often find poorly maintained secrets where the needs of secret consumers or producers mismatch. Therefore, you must standardize and centralize the secrets management solution with care. Standardizing and centralizing can mean that you use multiple secret management solutions. For instance: your cloud-native development teams choose to use the solution provided by the cloud provider, while your private cloud uses a third-party solution, and everybody has an account for a selected password manager.
By making sure that the teams standardize the interaction with these different solutions, they remain maintainable and usable in the event of an incident.
Even when a company centralizes its secrets management to just one solution, you will often have to secure the primary secret of that secrets management solution in a secondary secrets management solution. For instance, you can use a cloud provider's facilities to store secrets, but that cloud provider's root/management credentials need to be stored somewhere else.

Standardization should include Secrets life cycle management, Authentication, Authorization, and Accounting of the secrets management solution, and life cycle management. Note that it should be immediately apparent to an organization what a secret is used for and where to find it. The more Secrets management solutions you use, the more documentation you need.

### 2.3 Access Control

When users can read and/or update the secret in a secret management system, it means that the secret can now leak through that user and the system they used to touch the secret.
Therefore, engineers should not have access to all secrets in the secrets management system, and the Least Privilege principle should be applied. The secret management system needs to provide the ability to configure fine-grained access controls on each object and component to accomplish the Least Privilege principle.

### 2.4 Automate Secrets Management

Manual maintenance not only increases the risk of leakage; it also introduces the risk of human errors while maintaining the secret. Furthermore, it can become wasteful.
Therefore, it is better to limit or remove the human interaction with the actual secrets. You can restrict human interaction in multiple ways:

- **Secrets pipeline:** Having a secrets pipeline that does large parts of the secret management (e.g., creation, rotation, etc.)
- **Using dynamic secrets:** When an application starts, it could request its database credentials, which, when dynamically generated, will be provided with new credentials for that session. Dynamic secrets should be used where possible to reduce the surface area of credential reuse. Configure a short [lease duration](https://developer.hashicorp.com/vault/docs/concepts/lease) and revoke credentials when they are no longer needed. Restarting the application does not itself revoke stolen credentials; they remain usable until the backing service expires or revokes them.
- **Automated rotation of static secrets:** Key rotation is a challenging process when implemented manually, and can lead to mistakes. It is therefore better to automate the rotation of keys or at least ensure that the process is sufficiently supported by IT.

Rotating certain keys, such as encryption keys, might trigger full or partial data re-encryption. Different strategies for rotating keys exist:

- Gradual rotation
- Introducing new keys for Write operations
- Leaving old keys for Read operations
- Rapid rotation
- Scheduled rotation
- and more...

#### 2.4.1 Architectural Patterns for Automated Rotation

To illustrate how to design systems that support automated secret rotation, here are a few architectural patterns:

##### Example 1: Kubernetes with a Sidecar Container

In a Kubernetes environment, a common pattern is to use a sidecar container that is responsible for retrieving secrets from a secrets manager and making them available to the main application container. This decouples the application from the specifics of the secrets management solution.

- **Architecture:**
    - A Pod contains two containers: the main application container and a sidecar container (e.g., HashiCorp Vault Agent, CyberArk Conjur Secrets Provider).
    - The sidecar container authenticates with the secrets manager (e.g., using a Kubernetes Service Account).
    - It retrieves the secret and writes it to a shared in-memory volume.
    - The application container reads the secret from the shared volume.
    - The sidecar container can periodically refresh the secret, ensuring the application always has a valid, short-lived credential.
- **Kubernetes Manifest Snippet:**

    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: my-app
    spec:
      serviceAccountName: my-app-sa
      containers:
      - name: my-app-container
        image: my-app-image
        volumeMounts:
        - name: secrets-volume
          mountPath: "/mnt/secrets"
          readOnly: true
      - name: vault-agent-sidecar
        image: vault:latest
        args: ["agent", "-config=/etc/vault/vault-agent-config.hcl"]
        volumeMounts:
        - name: secrets-volume
          mountPath: "/mnt/secrets"
      volumes:
      - name: secrets-volume
        emptyDir:
          medium: "Memory"
    ```

##### Example 2: Serverless Function for Database Credential Rotation

Cloud-native secret managers often provide built-in support for automated rotation using serverless functions (e.g., AWS Lambda, Azure Functions).

- **Architecture:**
    - A secret is stored in a cloud secrets manager (e.g., AWS Secrets Manager).
    - The secrets manager is configured to trigger a rotation Lambda function on a schedule.
    - The Lambda function has the necessary permissions to update the database password and the secret value in the secrets manager.
    - The rotation process typically involves multiple steps (create new secret, set new secret, test new secret, finish rotation) to ensure a safe transition.

For AWS, start from the [rotation function templates](https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html). Secrets Manager invokes the function [separately for each rotation step](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_lambda.html); retrieve the pending credential from the secret version identified by `ClientRequestToken`, rather than relying on a local variable from an earlier invocation.

Follow the [rotation function security checks](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_lambda-functions.html) and [template validation](https://github.com/aws-samples/aws-secrets-manager-rotation-lambdas/blob/master/SecretsManagerRotationTemplate/lambda_function.py): ensure rotation is enabled and the request token identifies a known secret version. Safely return if that version is already `AWSCURRENT`; otherwise, require `AWSPENDING`. Before changing credentials, validate the current credential and confirm that the pending version targets the intended database and user under the chosen rotation strategy. These checks prevent the privileged function from being redirected to another resource. Test the pending credential before promoting its version to `AWSCURRENT`.

These examples demonstrate how you can create architectures that not only manage secrets securely but also automate the rotation process, significantly reducing the risk of compromised credentials.

### 2.5 Handling Secrets in Memory

An additional level of security can be achieved by minimizing the time window
where a secret is in memory and limiting the access to its memory space.

Depending on your application's particular circumstances, this can be difficult
to implement in a manner that ensures memory security. Because of this potential
implementation complexity, you are first encouraged to develop a threat model in order to clearly
surface your implicit assumptions about both your application's deployment environment as well
as understand the capabilities of your adversaries.

Often attempting to protect secrets in memory will be considered overkill
because as you evaluate a threat model, the potential threat
actors that you consider either do not have the capabilities to carry out such attacks
or the cost of defense far exceeds the likely impact of a compromise arising from
exposing secrets in memory. Also, it should be kept in mind while developing an
appropriate threat model, that if an attacker already has access to the memory of
the process handling the secret, by that time a security breach may have already
occurred. Furthermore, it should be recognized that with the advent of attacks like
[Rowhammer](https://arxiv.org/pdf/2211.07613.pdf), or
[Meltdown and Spectre](https://meltdownattack.com/), it is important
to understand that the operating system alone is not sufficient to protect your process
memory from these types of attacks. This becomes especially important when your
application is deployed to the cloud. The only foolproof approach to protecting memory
against these and similar attacks is to fully physically isolate your process memory from all other
untrusted processes.

Despite the implementation difficulties, in highly sensitive
environments, protecting secrets in memory can
be a valuable additional layer of security. For example, in scenarios where an
advanced attacker can cause a system to crash and gain access to a memory dump,
they may be able to extract secrets from it. Therefore, carefully safeguarding
secrets in memory is recommended for untrusted environments or situations where
tight security is of utmost importance.

Furthermore, in lower-level languages like C/C++, it is relatively easy to protect
secrets in memory. Thus, it may be worthwhile to implement this practice even if
the risk of an attacker gaining access to the memory is low. On the other hand, for
programming languages that rely on garbage collection, securing secrets in memory
generally is much more difficult.

- **Structures and Classes:** In .NET and Java, do not use immutable structures
    such as Strings to store secrets, since it is impossible to force them to
    be garbage collected. Instead, use primitive types such as byte arrays or
    char arrays, where the memory can be directly overwritten.

- **Zeroing Memory:** After a secret has been used, the memory it occupied
  should be zeroed out to prevent it from lingering in memory where it could
  potentially be accessed.

- **Memory Encryption:** In some cases, it may be possible to use hardware or
  operating system features to encrypt the entire memory space of the process
  handling the secret. This can provide an additional layer of security.

Remember, the goal is to minimize the time window where the secret is in
plaintext in memory as much as possible.

For more detailed information, see
[Testing Memory for Sensitive Data](https://mas.owasp.org/MASTG/tests/android/MASVS-STORAGE/MASTG-TEST-0011)
from the OWASP MAS project.

### 2.6 Auditing

Auditing is an essential part of secrets management due to the nature of the application. You must implement auditing securely to be resilient against attempts to tamper with or delete the audit logs. At a minimum, you should audit the following:

- Who requested a secret and for what system and role.
- Whether the secret request was approved or rejected.
- When the secret was used and by whom/what.
- When the secret has expired.
- Whether there were any attempts to reuse expired secrets.
- If there have been any authentication or authorization errors.
- When the secret was updated and by whom/what.
- Any administrative actions and possible user activity on the underlying supporting infrastructure stack.

It is essential that all auditing has correct timestamps. Therefore, the secret management solution should have proper time sync protocols set up at its supporting infrastructure. You should monitor the stack on which the solution runs for possible clock-skew and manual time adjustments.

### 2.7 Secret Lifecycle

Secrets follow a lifecycle. The stages of the lifecycle are as follows:

- Creation
- Rotation
- Revocation
- Expiration

#### 2.7.1 Creation

New secrets must be securely generated and cryptographically robust enough for their purpose. Secrets must have the minimum privileges assigned to them to enable their required use/role.

You should transmit credentials securely, such that ideally, you don't send the password along with the username when requesting user accounts. Instead, you should send the password via a secure channel (e.g., mutually authenticated connection) or a side-channel such as push notification, SMS, email. Refer to the [Multi-Factor Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet) to learn about the pros and cons of each channel.

Applications may not benefit from having multiple communication channels, so you must provision credentials securely.

See [the Open CRE project on secrets lookup](https://www.opencre.org/cre/223-780) for more technical recommendations on secret creation.

#### 2.7.2 Rotation

You should regularly rotate secrets so that any stolen credentials will only work for a short time. Regular rotation will also reduce the tendency for users to fall back to bad habits such as reusing credentials.

Depending on a secret's function and what it protects, the lifetime could be from minutes (think end-to-end encrypted chats with perfect forward secrecy) to years (consider hardware secrets).

User credentials are excluded from regular rotation. These should only be rotated if there is suspicion or evidence that they have been compromised, according to [NIST recommendations](https://pages.nist.gov/800-63-FAQ/#q-b05).

#### 2.7.3 Revocation

When secrets are no longer required or potentially compromised, you must securely revoke them to restrict access. With (TLS) certificates, this also involves certificate revocation.

#### 2.7.4 Expiration

You should create secrets to expire after a defined time where possible. This expiration can either be active expiration by the secret consuming system, or an expiration date set at the secrets management system forcing supporting processes to be triggered, resulting in a secret rotation.
You should apply policies through the secrets management solution to ensure credentials are only made available for a limited time appropriate for the type of credentials. Applications should verify that the secret is still active before trusting it.

### 2.8 Transport Layer Security (TLS) Everywhere

Never transmit secrets via plaintext. In this day and age, there is no excuse given the ubiquitous adoption of TLS.

Furthermore, you can effectively use secrets management solutions to provision TLS certificates.

### 2.9 Downtime, Break-glass, Backup and Restore

Consider the possibility that a secrets management service becomes unavailable for various reasons, such as scheduled downtime for maintenance. It could be impossible to retrieve the credentials required to restore the service if you did not previously acquire them. Thus, choose maintenance windows carefully based on earlier metrics and audit logs.

Next, the backup and restore procedures of the system should be regularly tested and audited for their security. A few requirements regarding backup & restore. Ensure that:

- An automated backup procedure is in place and executed periodically; base the frequency of the backups and snapshots on the number of secrets and their lifecycle.
- Frequently test restore procedures to guarantee that the backups are intact.
- Encrypt backups and put them on secure storage with reduced access rights. Monitor the backup location for (unauthorized) access and administrative actions.

Lastly, you should implement emergency ("break-glass") processes to restore the service if the system becomes unavailable for reasons other than regular maintenance. Therefore, emergency break-glass credentials should be regularly backed up securely in a secondary secrets management system and tested routinely to verify they work.

### 2.10 Policies

Consistently enforce policies defining the minimum complexity requirements of passwords and approved encryption algorithms at an organization-wide level. Using a centralized secrets management solution can help companies implement these policies.

Next, having an organization-wide secrets management policy can help enforce applying the best practices defined in this cheat sheet.

### 2.11 Metadata: prepare to move the secret

A secret management solution should provide the capability to store at least the following metadata about a secret:

- When it was created/consumed/archived/rotated/deleted
- Who created/consumed/archived/rotated/deleted it (e.g., both the actual producer and the engineer using the production method)
- What created/consumed/archived/rotated/deleted it
- Who to contact when having trouble with the secret or having questions about it
- For what the secret is used (e.g., designated intended consumers and purpose of the secret)
- What type of secret it is (e.g., AES Key, HMAC key, RSA private key)
- When you need to rotate it, if done manually

Note: if you don't store metadata about the secret nor prepare to move, you will increase the probability of vendor lock-in.

### 2.12 Passwordless Authentication and Token Security

OpenID Connect (OIDC) lets an application delegate user authentication to an identity provider (IdP), instead of storing and verifying the user's password itself. It does not require passwordless authentication: [OpenID Connect Core Section 3.1.2.3](https://openid.net/specs/openid-connect-core-1_0.html#Authenticates) leaves the IdP's authentication method, including passwords, outside the protocol's scope.

OIDC alone does not eliminate phishing, credential stuffing, or weak passwords at the IdP. Choose an IdP that enforces appropriate authentication controls; for phishing resistance, require [phishing-resistant authentication](https://pages.nist.gov/800-63-4/sp800-63b/authenticators/#verifimpers), such as WebAuthn. See the [Multifactor Authentication Cheat Sheet](Multifactor_Authentication_Cheat_Sheet.md).

Federation still requires protecting issued tokens and any client credentials. Follow the [OAuth2 Cheat Sheet](OAuth2_Cheat_Sheet.md) for token transmission, storage, validation, expiration, and refresh-token protection. OIDC does not replace other application secrets, such as database credentials or API keys.

## 3 Continuous Integration (CI) and Continuous Deployment (CD)

Building, testing and deploying changes generally requires access to many systems. Continuous Integration (CI) and Continuous Deployment (CD) tools typically store secrets to provide configuration to the application or during deployment. Alternatively, they interact heavily with the secrets management system. Various best practices can help smooth out secret management in CI/CD; we will deal with some of them in this section.

### 3.1 Hardening your CI/CD pipeline

CI/CD tooling consumes (high-privilege) credentials regularly. Ensure that the pipeline cannot be easily hacked or misused by employees. Here are a few guidelines which can help you:

- Treat your CI/CD tooling as a production environment: harden it, patch it and harden the underlying infrastructure and services.
- Have Security Event Monitoring in place.
- Implement least-privilege access: developers do not need to be able to administer projects. Instead, they only need to be able to execute required functions, such as setting up pipelines, running them, and working with code. Administrative tasks can quickly be done using configuration-as-code in a separate repository used by the CI/CD system to update its configuration. There is no need for privileged roles that might have access to secrets.
- Make sure that pipeline output does not leak secrets, and you can't listen in on production pipelines with debugging tools.
- Make sure you cannot exec into any runners and workers for a CI/CD system.
- Have proper authentication, authorization and accounting in place.
- Ensure only an approved process can create pipelines, including MR/PR steps to ensure that a created pipeline is security-reviewed.

### 3.2 Where should a secret be?

There are various places where you can store a secret to execute CI/CD actions:

- As part of your CI/CD tooling: you can store a secret in [GitLab](https://docs.gitlab.com/charts/installation/secrets.html)/[GitHub](https://docs.github.com/en/actions/security-guides/encrypted-secrets)/[Jenkins](https://www.jenkins.io/doc/developer/security/secrets/). This is not the same as committing it to code.
- As part of your secrets-management system: you can store a secret in a secrets management system, such as facilities provided by a cloud provider ([AWS Secrets Manager](https://aws.amazon.com/secrets-manager/), [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts), [Google Secret Manager](https://cloud.google.com/secret-manager)), or other third-party facilities ([Hashicorp Vault](https://www.vaultproject.io/), [Conjur](https://www.conjur.org/), [Keeper](https://www.keepersecurity.com/)). In this case, the CI/CD pipeline tooling requires credentials to connect to these secret management systems to have secrets in place. See [Cloud Providers](#4-cloud-providers) for more details on using a cloud provider's secret management system.

Another alternative here is using the CI/CD pipeline to leverage the Encryption as a Service from the secrets management systems to do the encryption of a secret. The CI/CD tooling can then commit the encrypted secret to git, which can be fetched by the consuming service on deployment and decrypted again. See section 3.6 for more details.

Note: not all secrets must be in the CI/CD pipeline to get to the actual deployment. Instead, make sure that the deployed services take care of part of their secrets management at their own lifecycle (e.g., deployment, runtime and destruction).

#### 3.2.1 As part of your CI/CD tooling

When secrets are part of your CI/CD tooling, it means that these secrets are exposed to your CI/CD jobs. CI/CD tooling can comprise, e.g., GitHub secrets, GitLab repository secrets, ENV Vars/Var Groups in Microsoft Azure DevOps, Kubernetes Secrets, etc.
These secrets are often configurable/viewable by people who have the authorization to do so (e.g., a maintainer in GitHub, a project owner in GitLab, an admin in Jenkins, etc.), which together line up for the following best practices:

- No "big secret": ensure that secrets in your CI/CD tooling that are not long-term, don't have a wide blast radius, and don't have a high value. Also, limit shared secrets (e.g., never have one password for all administrative users).
- As is / To be: have a clear overview of which users can view or alter the secrets. Often, maintainers of a GitLab/GitHub project can see or otherwise extract its secrets.
- Reduce the number of people that can perform administrative tasks on the project to limit exposure.
- Log & Alert: Assemble all the logs from the CI/CD tooling and have rules in place to detect secret extraction or misuse, whether through accessing them through a web interface or dumping them while double Base64 encoding or encrypting them with OpenSSL.
- Rotation: Regularly rotate secrets.
- Forking should not leak: Validate that a fork of the repository or copy of the job definition does not copy the secret.
- Document: Make sure you document which secrets you store as part of your CI/CD tooling and why so that you can migrate these easily when required.

#### 3.2.2 Storing it in a secrets management system

Naturally, you can store secrets in a designated secrets management solution. For example, you can use a solution offered by your (cloud) infrastructure provider, such as [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/), [Google Secrets Manager](https://cloud.google.com/secret-manager), or [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts). You can find more information about these in [section 4](#4-cloud-providers) of this cheat sheet. Another option is a dedicated secrets management system, such as [Hashicorp Vault](https://www.vaultproject.io/), [Keeper](https://www.keepersecurity.com/), [Conjur](https://www.conjur.org/).
Here are a few do's and don'ts for the CI/CD interaction with these systems. Make sure that the following is taken care of:

- Rotation/Temporality: credentials used by the CI/CD tooling to authenticate against the secret management system are rotated frequently and expire after a job completes.
- Scope of authorization: scope credentials used by the CI/CD tooling (e.g., roles, users, etc.), only authorize those secrets and services of the secret management system required for the CI/CD tooling to execute its job.
- Attribution of the caller: credentials used by the CI/CD tooling still hold attribution of the one calling the secrets management solution. Ensure you can attribute any calls made by the CI/CD tooling to a person or service that requested the actions of the CI/CD tooling. If this is not possible through the default configuration of the secrets manager, make sure that you have a correlation setup in terms of request parameters.
- All of the above: Still follow those do's and don'ts listed in section 3.2.1: log & alert, take care of forking, etc.
- Backup: back up secrets to product-critical operations in separate storage (e.g., cold storage), especially encryption keys.

#### 3.2.3 Not touched by CI/CD at all

Secrets do not necessarily need to be brought to a consumer of the secret by a CI/CD pipeline. It is even better when the consumer of the secret retrieves the secret. In that case, the CI/CD pipeline still needs to instruct the orchestrating system (e.g., [Kubernetes](https://kubernetes.io/)) that it needs to schedule a specific service with a given service account with which the consumer can then retrieve the required secret. The CI/CD tooling then still has credentials for the orchestrating platform but no longer has access to the secrets themselves. The do's and don'ts regarding these credentials types are similar to those described in section 3.2.2.

### 3.3 Authentication and Authorization of CI/CD tooling

CI/CD tooling should have designated service accounts, which can only operate in the scope of the required secrets or orchestration of the consumers of a secret. Additionally, a CI/CD pipeline run should be easily attributable to the one who has defined the job or triggered it to detect who has tried to exfiltrate secrets or manipulate them. When you use certificate-based auth, the caller of the pipeline identity should be part of the certificate. If you use a token to authenticate towards the mentioned systems, make sure you set the principal requesting these actions (e.g., the user or the job creator).

Verify on a periodic basis whether this is (still) the case for your system so that you can do logging, attribution, and security alerting on suspicious actions effectively.

### 3.4 Logging and Accounting

Attackers can use CI/CD tooling to extract secrets. They could, for example, use administrative interfaces or job creation that exfiltrates the secret using encryption or double Base64 encoding. Therefore, you should log every action in a CI/CD tool. You should define security alerting rules at every non-standard manipulation of the pipeline tool and its administrative interface to monitor secret usage.
Logs should be queryable for at least 90 days and stored for a more extended period in cold storage. It might take security teams time to understand how attackers can exfiltrate or manipulate a secret using CI/CD tooling.

### 3.5 Rotation vs Dynamic Creation

You can leverage CI/CD tooling to rotate secrets or instruct other components to do the rotation of the secret. For instance, the CI/CD tool can request a secrets management system or another application to rotate the secret. Alternatively, the CI/CD tool or another component could set up a dynamic secret: a secret required for a consumer to use for as long as it lives. Tie invalidation to the provider's [lease expiry or explicit revocation](https://developer.hashicorp.com/vault/docs/concepts/lease); stopping the consumer alone does not revoke the secret. This procedure reduces possible leakage of a secret and allows for easy detection of misuse. If an attacker uses a secret from anywhere other than the consumer's IP, you can easily detect it.

### 3.6 Pipeline Created Secrets

You can use pipeline tooling to generate secrets and either offer them directly to the service deployed by the tooling or provide the secret to a secrets management solution. Alternatively, the secret can be stored encrypted in git so that the secret and its metadata is as close to the developer's daily place of work as possible. A git-stored secret does require that developers cannot decrypt the secrets themselves and that every consumer of a secret has its encrypted variant of the secret. For instance: the secret should then be different per DTAP environment and be encrypted with another key. For each environment, only the designated consumer in that environment should be able to decrypt the specific secret. A secret does not leak cross-environment and can still be easily stored next to the code.
Consumers of a secret could now decrypt the secret using a sidecar, as described in section 5.2. Instead of retrieving the secrets, the consumer would leverage the sidecar to decrypt the secret.

When a pipeline creates a secret by itself, ensure that the scripts or binaries involved adhere to best practices for secret generation. Best practices include secure randomness, proper length of secret creation, etc. and that the secret is created based on well-defined metadata stored somewhere in git or somewhere else.

## 4 Cloud Providers

For cloud providers, there are at least four essential topics to touch upon:

- Designated secret storage/management solutions. Which service(s) do you use?
- Envelope & client-side encryption
- Identity and access management: decreasing the blast radius
- API quotas or service limits

### 4.1 Services to Use

It is best to use a designated secret management solution in any environment. Most cloud providers have at least one service that offers secret management. Of course, it's also possible to run a different secret management solution (e.g., HashiCorp Vault or Conjur) on compute resources within the cloud. We'll consider cloud provider service offerings in this section.

Sometimes it's possible to automatically rotate your secret, either via a service provided by your cloud provider or a (custom-built) function. Generally, you should prefer the cloud provider's solution since the barrier of entry and risk of misconfiguration are lower. If you use a custom solution, ensure the function's role to do its rotation can only be assumed by said function.

#### 4.1.1 AWS

For AWS, the recommended solution is [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html).

Permissions are granted at the secret level. Check out the [Secrets Manager best practices](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html).

It is also possible to use the [Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html), which is cheaper, but that has a few downsides:

- you'll need to make sure you've specified encryption yourself (secrets manager does that by default)
- it offers fewer auto-rotation capabilities (you will likely need to build a custom function)
- cross-account sharing is limited to [advanced parameters](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-shared-parameters.html); sharing encrypted `SecureString` values also requires a customer managed AWS KMS key and separately granting access to that key
- it doesn't support cross-region replication
- there are fewer [Security Hub Controls](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html) available

##### 4.1.1.1 AWS Nitro Enclaves

With [AWS Nitro Enclaves](https://aws.amazon.com/ec2/nitro/nitro-enclaves/), you can create isolated compute environments to further protect and securely process highly sensitive data such as secrets. Enclaves are hardened, and restrict operator access, providing a trusted execution environment. A key feature is cryptographic attestation, which allows you to verify the enclave's identity and ensure only authorized code is running before provisioning secrets to it. This makes it a strong choice for scenarios requiring high assurance in secret handling.

##### 4.1.1.2 AWS CloudHSM

For secrets being used in highly confidential applications, it may be needed to have more control over the encryption and storage of these keys. AWS offers [CloudHSM](https://aws.amazon.com/cloudhsm/), which lets you bring your own key (BYOK) for AWS services. Thus, you will have more control over keys' creation, lifecycle, and durability. Scale a CloudHSM cluster by [adding or removing HSMs](https://docs.aws.amazon.com/cloudhsm/latest/userguide/add-remove-hsm.html); the service makes [periodic encrypted backups of cluster users, keys, and configuration](https://docs.aws.amazon.com/cloudhsm/latest/userguide/manage-backups.html). The cloud service provider, Amazon, will not have any access to the key material stored in **AWS CloudHSM**.

#### 4.1.2 GCP

For GCP, the recommended service is [Secret Manager](https://cloud.google.com/secret-manager/docs).

Permissions are granted at the secret level.

Check out the [Secret Manager best practices](https://cloud.google.com/secret-manager/docs/best-practices).

##### 4.1.2.1 Google Cloud Confidential Computing

[GCP Confidential Computing](https://cloud.google.com/confidential-computing) is a technology that encrypts data in-use, while it is being processed. This is achieved through services like **Confidential VMs** and **Confidential GKE Nodes**, which leverage AMD Secure Encrypted Virtualization (SEV). This ensures that even Google personnel cannot view the contents of the memory of your virtual machines, providing a high degree of protection for secrets that must be held in memory.

#### 4.1.3 Azure

For Azure, the recommended service is [Key Vault](https://docs.microsoft.com/en-us/azure/key-vault/).

Azure's [role-based access control (RBAC)](https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide) supports role assignments for individual secrets, keys, and certificates. Follow the [Identity and Access Management guidance](#43-identity-and-access-management-iam) for access scopes and vault boundaries.

Check out the [Key Vault best practices](https://docs.microsoft.com/en-us/azure/key-vault/general/best-practices).

##### 4.1.3.1 Azure Confidential Computing

With [Azure Confidential Computing](https://azure.microsoft.com/en-us/solutions/confidential-compute/#overview), you can create trusted execution environments. This technology isolates sensitive data within a protected container, ensuring that it is encrypted both at rest, in transit, and in use. Services like **Azure Confidential Virtual Machines** and **Confidential Containers on ACI** utilize technologies like Intel SGX and AMD SEV-SNP to create these secure enclaves. This prevents unauthorized access from cloud administrators, malware, or other tenants, making it a robust solution for secret management.

##### 4.1.3.2 Azure Dedicated HSM

For secrets being used in Azure environments and requiring special security considerations, Azure offers [Azure Dedicated HSM](https://azure.microsoft.com/en-us/services/azure-dedicated-hsm/). This allows you more control over the secrets stored on it, including enhanced administrative and cryptographic control. The cloud service provider, Microsoft, will not have any access to the key material stored in Azure Dedicated HSM.

#### 4.1.4 Other clouds, Multi-cloud, and Cloud agnostic

If you're using multiple cloud providers, you should consider using a cloud-agnostic secret management solution. This will allow you to use the same secret management solution across all your cloud providers (and possibly also on-premises). Another advantage is that this avoids vendor lock-in with a specific cloud provider, as the solution can be used on any cloud provider.

There are open-source and commercial solutions available. Some examples are:

- [CyberArk Conjur](https://www.conjur.org/)
- [HashiCorp Vault](https://www.vaultproject.io/)
- [Pulumi ESC](https://www.pulumi.com/esc/)

### 4.2 Envelope & client-side encryption

This section will describe how a secret is encrypted and how you can manage the keys for that encryption in the cloud.

#### 4.2.1 Client-side encryption versus server-side encryption

Server-side encryption of secrets ensures that the cloud provider takes care of the encryption of the secret in storage. The secret is then safeguarded against compromise while at rest. Encryption at rest often does not require additional work other than selecting the key to encrypt it with (See section 4.2.2). However, when you submit the secret to another service, it will no longer be encrypted. It is decrypted before sharing with the intended service or human user.

Client-side encryption of secrets ensures that the secret remains encrypted until you actively decrypt it. This means it is only decrypted when it arrives at the consumer. You need to have a proper crypto system to cater for this. Think about mechanisms such as PGP using a safe configuration and other more scalable and relatively easy to use systems. Client-side encryption can provide an end-to-end encryption of the secret: from producer to consumer.

#### 4.2.2 Bring Your Own Key versus Cloud Provider Key

When you encrypt a secret at rest, the question is: which key do you want to use? The less trust you have in the cloud provider, the more you will want to manage yourself.

Often, you can either encrypt a secret with a key managed at the secrets management service or use a key management solution from the cloud provider to encrypt the secret. The key offered through the key management solution of the cloud provider can be either managed by the cloud provider or by yourself. Industry standards call the latter "bring your own key" (BYOK). You can either directly import or generate this key at the key management solution or using cloud HSM supported by the cloud provider.
You can then either use your key or the customer main key from the provider to encrypt the data key of the secrets management solution. The data key, in turn, encrypts the secret. By managing the CMK, you have control over the data key at the secrets management solution.

While importing your own key material can generally be done with all providers ([AWS](https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys.html), [Azure](https://docs.microsoft.com/en-us/azure/key-vault/keys/byok-specification), [GCP](https://cloud.google.com/kms/docs/key-import)), unless you know what you are doing and your threat model and policy require this, this is not a recommended solution due to its complexity and difficulty of use.

### 4.3 Identity and Access Management (IAM)

IAM applies to both on-premises and cloud setups: to effectively manage secrets, you need to set up suitable access policies and roles. Setting this up goes beyond policies regarding secrets; it should include hardening the full IAM setup, as it could otherwise allow for privilege escalation attacks. Ensure you never allow open "pass role" privileges or unrestricted IAM creation privileges, as these can use or create credentials that have access to the secrets. Next, make sure you tightly control what can impersonate a service account: are your machines' roles accessible by an attacker exploiting your server? Can service roles from the data-pipeline tooling access the secrets easily? Ensure you include IAM for every cloud component in your threat model (e.g., ask yourself: how can you do elevation of privileges with this component?). See [this blog entry](https://xebia.com/ten-pitfalls-you-should-look-out-for-in-aws-iam/) for multiple do's and don'ts with examples.

Leverage the temporality of the IAM principals effectively: e.g., ensure that only specific roles and service accounts that require it can access the secrets. Monitor these accounts so that you can tell who or what used them to access the secrets.

Next, make sure that you scope access to your secrets: one should not be simply allowed to access all secrets. In GCP and AWS, you can create fine-grained access policies to ensure that a principal cannot access all secrets at once. For Azure Key Vault, use the recommended [Azure RBAC permission model](https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide) with least-privilege roles. Azure RBAC supports role assignments at the scope of individual keys, secrets, and certificates for limited sharing scenarios, but Microsoft recommends [separate vaults per application and environment](https://learn.microsoft.com/en-us/azure/key-vault/general/secure-key-vault) as the primary security boundary.

### 4.4 API limits

Cloud services can generally provide a limited amount of API calls over a given period. You could potentially (D)DoS yourself when you run into these limits. Most of these limits apply per account, project, or subscription, so spread workloads to limit your blast radius accordingly. Additionally, some services may support data key caching, preventing load on the key management service API (see, for example, [AWS data key caching](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/data-key-caching.html)). Some services can leverage built-in data key caching. [S3 is one such example](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-key.html).

## 5 Containers & Orchestrators

You can enrich containers with secrets in multiple ways: build time (not recommended) and during orchestration/deployment.

### 5.1 Injection of Secrets (file, in-memory)

There are three ways to get secrets to an app inside a Docker container.

- Mounted volumes (file): With this method, we keep our secrets within a particular config/secret file and mount that file to our instance as a mounted volume. Ensure that these mounts are mounted in by the orchestrator and never built-in, as this will leak the secret with the container definition. Instead, make sure that the orchestrator mounts in the volume when required.
- Fetch from the secret store (in-memory): A sidecar app/container fetches the secrets it needs directly from a secret manager service without dealing with docker config. This solution allows you to use dynamically constructed secrets without worrying about the secrets being viewable from the file system or from checking the Docker container's environment variables.
- Environment variables: We can provide secrets directly as part of the Docker container configuration. Note: secrets themselves should never be hardcoded using docker ENV or docker ARG commands, as these can easily leak with the container definitions. See the Docker challenges at [WrongSecrets](https://github.com/OWASP/wrongsecrets) as well. Instead, let an orchestrator overwrite the environment variable with the actual secret and ensure that this is not hardcoded. Additionally, environment variables are generally accessible to all processes and may be included in logs or system dumps. Using environment variables is therefore not recommended unless the other methods are not possible.

### 5.2 Short-Lived Sidecar Containers

To inject secrets, you could create short-lived sidecar containers that fetch secrets from some remote endpoint and then store them on a shared volume mounted to the original container. The original container can now use the secrets from the mounted volume. The benefit of using this approach is that we don't need to integrate any third-party tool or code to get secrets. Once the sidecar has fetched the secrets, it terminates. Examples of this include [Vault Agent Sidecar Injector](https://developer.hashicorp.com/vault/docs/platform/k8s/injector) and [Conjur Secrets Provider](https://github.com/cyberark/secrets-provider-for-k8s). By mounting secrets to a volume shared with the pod, containers within the pod can consume secrets without being aware of the secrets manager.

### 5.3 Internal vs External Access

You should only expose secrets to communication mechanisms between the container and the deployment representation (e.g., a Kubernetes Pod). Never expose secrets through external access mechanisms shared among deployments or orchestrators (e.g., a shared volume).

When the orchestrator stores secrets (e.g., Kubernetes Secrets), make sure that the storage backend of the orchestrator is encrypted and you manage the keys well. See the [Kubernetes Security Cheat Sheet](Kubernetes_Security_Cheat_Sheet.md) for more information.

## 6 Implementation Guidance

In this section, we will discuss implementation. Note that it is always best to refer to the official documentation of the secrets management system of choice for the actual implementation as it will be more up to date than any secondary document such as this cheat sheet.

### 6.1 Key Material Management Policies

Key material management is discussed in the [Key Management Cheat Sheet](Key_Management_Cheat_Sheet.md)

### 6.2 Dynamic vs Static Use Cases

We see the following use cases for dynamic secrets, among others:

- short-lived secrets (e.g., credentials or API keys) for a secondary service that expresses the intent for connecting the primary service (e.g., consumer) to the service.
- short-lived integrity and encryption controls for guarding and securing in-memory and runtime communication processes. Think of encryption keys that only need to live for a single session or a single deployment lifetime.
- short-lived credentials for building a stack during the deployment of a service for interacting with the deployers and supporting infrastructure.

Note that these dynamic secrets often need to be created with the service we need to connect to. To create these types of dynamic secrets, we usually require long-term static secrets to create the dynamic secrets themselves. Other static use cases:

- key material that needs to live longer than a single deployment due to the nature of its usage in the interaction with other instances of the same service (e.g., storage encryption keys, TLS PKI keys)
- key material or credentials to connect to services that do not support creating temporal roles or credentials.

### 6.3 Ensure limitations are in place

Secrets should never be retrievable by everyone and everything. Always make sure that you put guardrails in place:

- Do you have the opportunity to create access policies? Ensure that there are policies in place to limit the number of entities that can read or write the secret. At the same time, write the policies so that you can easily extend them, and they are not too complicated to understand.
- Is there no way to reduce access to certain secrets within a secrets management solution? Consider separating the production and development secrets by having separate secret management solutions. Then, reduce access to the production secrets management solution.

### 6.4 Security Event Monitoring is Key

Continually monitor who/what, from which IP, and what methodology accesses the secret. There are various patterns to look out for, such as, but not limited to:

- Monitor who accesses the secret at the secret management system: is this normal behavior? If the CI/CD credentials are used to access the secret management solution from a different IP than where the CI/CD system is running, provide a security alert and assume the secret is compromised.
- Monitor the service requiring the secret (if possible), e.g., whether the user of the secret is coming from an expected IP, with an expected user agent. If not, alert and assume the secret is compromised.

### 6.5 Usability and Ease of Onboarding

For a secrets management solution to be effective, it must be easy for developers to adopt and use. If the process is too complex, developers may resort to insecure practices. A focus on usability and a smooth onboarding experience is critical.

- **Clear and Comprehensive Documentation:**
    - Provide clear, concise, and easy-to-find documentation. This should include tutorials for common use cases, detailed API references, and practical examples.
    - Maintain a "getting started" guide that walks new users through the process of obtaining their first secret.
- **Developer-Friendly Tooling and SDKs:**
    - Offer well-maintained SDKs for various programming languages to simplify integration.
    - Provide a command-line interface (CLI) that allows developers to manage secrets from their local development environment.
    - Develop plugins for common IDEs, CI/CD systems, and infrastructure-as-code (IaC) tools like Terraform and Pulumi.
- **Streamlined Workflows:**
    - Implement self-service workflows that enable developers to request and receive secrets with minimal manual intervention.
    - Use GitOps principles to manage secrets as code, allowing developers to define secret needs in a declarative manner alongside their application code.
    - Automate the approval process for low-risk secrets while maintaining appropriate controls for more sensitive ones.
- **Actionable Feedback and Support:**
    - Provide clear error messages that help developers troubleshoot issues independently.
    - Establish dedicated support channels (e.g., a Slack channel, a ticketing system) where developers can get help from the security or platform team.
- **Easy Integration:**
    - Ensure the secrets management solution can be easily integrated with existing applications. Sidecar containers, such as the [Vault Agent Sidecar Injector](https://developer.hashicorp.com/vault/docs/platform/k8s/injector) or the [Conjur Secrets Provider](https://github.com/cyberark/secrets-provider-for-k8s), can help decouple applications from the secrets management system.

## 7 Encryption

Secrets Management goes hand in hand with encryption. After all, secrets must be stored encrypted somewhere to protect their confidentiality and integrity.

### 7.1 Encryption Types to Use

You can use various encryption types to secure a secret as long as they provide sufficient security, including adequate resistance against quantum computing-based attacks. Given that this is a moving field, it is best to take a look at sources like [keylength.com](https://www.keylength.com/en/4/), which enumerate up-to-date recommendations on the usage of encryption types and key lengths for existing standards, as well as the NSA's [Commercial National Security Algorithm Suite 2.0](https://media.defense.gov/2022/Sep/07/2003071834/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS_.PDF) which enumerates quantum resistant algorithms.

Please note that in all cases, we need to preferably select an algorithm that provides encryption and confidentiality at the same time, such as AES-256 using GCM [(Galois Counter Mode)](https://en.wikipedia.org/wiki/Galois/Counter_Mode), or a mixture of ChaCha20 and Poly1305 according to the best practices in the field.

### 7.2 Convergent Encryption

[Convergent Encryption](https://en.wikipedia.org/wiki/Convergent_encryption) ensures that a given plaintext and its key results in the same ciphertext. This can help detect possible reuse of secrets, resulting in the same ciphertext.
The challenge with enabling convergent encryption is that it allows attackers to use the system to generate a set of cryptographic strings that might end up in the same secret, allowing the attacker to derive the plaintext secret. Given the algorithm and key, you can mitigate this risk if the convergent crypto system you use has sufficient resource challenges during encryption. Another factor that can help reduce the risk is ensuring that a secret is of adequate length, further hampering the possible guess-iteration time required.

### 7.3 Where to store the Encryption Keys?

You should not store keys next to the secrets they encrypt, except if those keys are encrypted themselves (see envelope encryption). Start by consulting the [Key Management Cheat Sheet](Key_Management_Cheat_Sheet.md) on where and how to store the encryption and possible HMAC keys.

### 7.4 Encryption as a Service (EaaS)

EaaS is a model in which users subscribe to a cloud-based encryption service without having to install encryption on their own systems. Using EaaS, you can get the following benefits:

- Encryption at rest
- Encryption in transit (TLS)
- Key handling and cryptographic implementations are taken care of by Encryption Service, not by developers
- The provider could add more services to interact with the sensitive data

## 8 Detection

There are many approaches to secrets detection and some very useful open-source projects to help with this. The [Yelp Detect Secrets](https://github.com/Yelp/detect-secrets) project is mature and has signature matching for around 20 secrets. For more information on other tools to help you in the detection space, check out the [Secrets Detection](https://github.com/topics/secrets-detection) topic on GitHub.

### 8.1 General detection approaches

Shift-left and DevSecOps principles apply to secrets detection as well. These general approaches below aim to consider secrets earlier and evolve the practice over time.

- Create standard test secrets and use them universally across the organization. This allows for reducing false positives by only needing to track a single test secret for each secret type.
- Consider enabling secrets detection at the developer level to avoid checking secrets into code before commit/PR either in the IDE, as part of test-driven development, or via pre-commit hook.
- Make secrets detection part of the threat model. Consider secrets as part of the attack surface during threat modeling exercises.
- Evaluate detection utilities and related signatures often to ensure they meet expectations.
- Consider having more than one detection utility and correlating/de-duping results to identify potential areas of detection weakness.
- Explore a balance between entropy and ease of detection. Secrets with consistent formats are easier to detect with lower false-positive rates, but you also don't want to miss a human-created password simply because it doesn't match your detection rules.

### 8.2 Types of secrets to be detected

Many types of secrets exist, and you should consider signatures for each to ensure accurate detection for all. Among the more common types are:

- High availability secrets (Tokens that are difficult to rotate)
- Application configuration files
- Connection strings
- API keys
- Credentials
- Passwords
- 2FA keys
- Private keys (e.g., SSH keys)
- Session tokens
- Platform-specific secret types (e.g., Amazon Web Services, Google Cloud)

For more fun learning about secrets and practice rooting them out, check out the [Wrong Secrets](https://owasp.org/www-project-wrongsecrets/) project.

### 8.3 Detection lifecycle

Secrets are like any other authorization token. They should:

- Exist only for as long as necessary (rotate often)
- Have a method for automatic rotation
- Only be visible to those who need them (least privilege)
- Be revocable (including the logging of attempt to use a revoked secret)
- Never be logged (must implement either an encryption or masking approach in place to avoid logging plaintext secrets)

Create detection rules for each of the stages of the secret lifecycle.

### 8.4 Documentation for how to detect secrets

Create documentation and update it regularly to inform the developer community on procedures and systems available at your organization and what types of secrets management you expect, how to test for secrets, and what to do in the event of detected secrets.

Documentation should:

- Exist and be updated often, especially in response to an incident
- Include the following information:
    - Who has access to the secret
    - How it gets rotated
    - Any upstream or downstream dependencies that could potentially be broken during secret rotation
    - Who is the point of contact during an incident
    - Security impact of exposure

- Identify when secrets may be handled differently depending on the threat risk, data classification, etc.

## 9 Incident Response

Quick response in the event of a secret exposure is perhaps one of the most critical considerations for secrets management.

### 9.1 Documentation

Incident response in the event of secret exposure should ensure that everyone in the chain of custody is aware and understands how to respond. This includes application creators (every member of a development team), information security, and technology leadership.

Documentation must include:

- How to test for secrets and secrets handling, especially during business continuity reviews.
- Whom to alert when a secret is detected.
- Steps to take for containment
- Information to log during the event

### 9.2 Remediation

The primary goal of incident response is rapid response and containment.

Containment should follow these procedures:

1. Revocation: Keys that were exposed should undergo immediate revocation. The secret must be able to be de-authorized quickly, and systems must be in place to identify the revocation status.
2. Rotation: A new secret must be able to be quickly created and implemented, preferably via an automated process to ensure repeatability, low rate of implementation error, and least-privilege (not directly human-readable).
3. Deletion: Secrets revoked/rotated must be removed from the exposed system immediately, including secrets discovered in code or logs. Secrets in code could have commit history for the exposure squashed to before the introduction of the secret, however, this may introduce other problems as it rewrites git history and will break any other links to a given commit. If you decide to do this be aware of the consequences and plan accordingly. Secrets in logs must have a process for removing the secret while maintaining log integrity.
4. Logging: Incident response teams must have access to information about the lifecycle of a secret to aid in containment and remediation, including:
    - Who had access?
    - When did they use it?
    - When was it previously rotated?

### 9.3 Logging

Additional considerations for logging of secrets usage should include:

- Logging for incident response should be to a single location accessible by incident response (IR) teams
- Ensure fidelity of logging information during purple team exercises such as:
    - What should have been logged?
    - What was actually logged?
    - Do we have adequate alerts in place to ensure this?

Consider using a standardized logging format and vocabulary such as the [Logging Vocabulary Cheat Sheet](Logging_Vocabulary_Cheat_Sheet.md) to ensure that all necessary information is logged.

## 10 Secrets Management in a Multi-Cloud Environment

### 10.1 Introduction

Managing secrets in a multi-cloud environment presents unique challenges due to the diversity of cloud providers and their respective services. This section discusses the challenges and best practices for managing secrets across multiple cloud providers.

### 10.2 Challenges

1. **Diverse APIs and Interfaces**: Each cloud provider has its own API and interface for managing secrets, which can lead to complexity in integrating and managing secrets across multiple providers.
2. **Inconsistent Security Policies**: Different cloud providers may have varying security policies and practices, making it challenging to enforce consistent security standards across all environments.
3. **Key Rotation**: Ensuring that keys are rotated consistently and securely across multiple cloud providers can be difficult, especially if each provider has different mechanisms for key rotation.
4. **Access Control**: Managing access control for secrets across multiple cloud providers can be complex, as each provider may have different access control mechanisms and policies.
5. **Auditing and Monitoring**: Ensuring comprehensive auditing and monitoring of secret access and usage across multiple cloud providers can be challenging due to the differences in logging and monitoring capabilities.

### 10.3 Best Practices

1. **Use a Centralized Secrets Management Solution**: Implement a centralized secrets management solution that can integrate with multiple cloud providers. This can help standardize the management of secrets and enforce consistent security policies across all environments. Examples include HashiCorp Vault and CyberArk Conjur.
2. **Standardize Security Policies**: Define and enforce standardized security policies for managing secrets across all cloud providers. This includes policies for key rotation, access control, and auditing.
3. **Automate Key Rotation**: Implement automated key rotation processes to ensure that keys are rotated consistently and securely across all cloud providers. Use tools and scripts to automate the rotation process and reduce the risk of human error.
4. **Implement Fine-Grained Access Control**: Use fine-grained access control mechanisms to restrict access to secrets based on the principle of least privilege. Ensure that access control policies are consistently enforced across all cloud providers.
5. **Enable Comprehensive Auditing and Monitoring**: Implement comprehensive auditing and monitoring of secret access and usage across all cloud providers. Use centralized logging and monitoring solutions to aggregate and analyze logs from multiple providers.

### 10.4 References

- [HashiCorp Vault](https://www.vaultproject.io/)
- [CyberArk Conjur](https://www.conjur.org/)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts)
- [Google Cloud Secret Manager](https://cloud.google.com/secret-manager)

## 11 Related Cheat Sheets & further reading

- [Key Management Cheat Sheet](Key_Management_Cheat_Sheet.md)
- [Logging Cheat Sheet](Logging_Cheat_Sheet.md)
- [Password Storage Cheat Sheet](Password_Storage_Cheat_Sheet.md)
- [Cryptographic Storage Cheat Sheet](Cryptographic_Storage_Cheat_Sheet.md)
- [OWASP WrongSecrets project](https://github.com/OWASP/wrongsecrets/)

## References

- [NIST SP 800-57 Part 1 Rev. 5: Recommendation for Key Management](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)
- [AWS Secrets Manager: Best practices](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- [Azure Key Vault: Secure your secrets](https://learn.microsoft.com/en-us/azure/key-vault/secrets/secure-secrets)

---

## Section 17: Secure Code Review Cheat Sheet

# Secure Code Review Cheat Sheet

## Introduction

**Secure Code Review** is the process of manually examining source code to identify security vulnerabilities that automated tools often miss. It involves analyzing application logic, data flow, and implementation details to detect security flaws that require human expertise and contextual understanding.

**Manual Code Review** complements automated security testing tools (SAST/DAST) by focusing on areas where human analysis provides the most value, including business logic validation, complex security implementations, and context-specific vulnerabilities. While automated tools can assist by highlighting potential areas of concern, the core analysis relies on human judgment and domain expertise.

**Security-Focused Review** differs from functional code review by specifically targeting security concerns such as input validation, authentication mechanisms, authorization controls, cryptographic implementations, and potential attack vectors.

### Review Types

**Baseline Reviews** examine the entire codebase comprehensively. Use for:

- New applications or major releases
- Legacy system onboarding
- Compliance requirements
- Post-incident analysis

**Diff-Based Reviews** focus on code changes only. Use for:

- Pull requests and commits
- Daily development workflow
- Feature completion
- Continuous security validation

This cheat sheet provides practical guidance for conducting effective manual security code reviews, with emphasis on both baseline and incremental review methodologies.

## Review Methodology

### Preparation

**For All Reviews:**

- Understand application architecture and business requirements
- Gather [threat models](Threat_Modeling_Cheat_Sheet.md) and previous security findings
- Identify critical assets and high-risk functions
- Review security requirements and documentation

**Additional for Baseline Reviews:**

- Map complete [application boundaries and dependencies](Attack_Surface_Analysis_Cheat_Sheet.md)
- Analyze overall security architecture
- Review security incident history
- Audit all third-party libraries

**Additional for Diff-Based Reviews:**

- Identify modified files and affected components
- Assess impact on existing security controls
- Understand purpose of changes
- Prioritize high-risk modifications

### Review Process

**Baseline Review Steps:**

1. Architecture review for security anti-patterns
2. Entry point analysis and input validation
3. Authentication and authorization verification
4. Data flow tracing
5. Business logic analysis
6. Cryptographic implementation review
7. Error handling verification
8. Configuration and deployment review

**Diff-Based Review Steps:**

1. Analyze impact on existing security controls
2. Identify new attack vectors
3. Verify security at modified trust boundaries
4. Check new integrations
5. Ensure no security regression
6. Apply relevant security patterns

## Common Vulnerability Patterns

For request forgery and redirect checks, also consult the [CSRF Prevention](Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.md), [SSRF Prevention](Server_Side_Request_Forgery_Prevention_Cheat_Sheet.md), and [Unvalidated Redirects and Forwards](Unvalidated_Redirects_and_Forwards_Cheat_Sheet.md) cheat sheets.

### Input Validation Vulnerabilities

Check for missing server-side validation, improper sanitization, and weak input filtering. For more information, see [Input Validation Cheat Sheet](Input_Validation_Cheat_Sheet.md) and [Mass Assignment Cheat Sheet](Mass_Assignment_Cheat_Sheet.md).

### Injection Vulnerabilities

**SQL Injection:**

Look for string concatenation in database queries and unsafe query construction. For more information, see [SQL Injection Prevention Cheat Sheet](SQL_Injection_Prevention_Cheat_Sheet.md).

**Cross-Site Scripting (XSS):**

Review output encoding, DOM manipulation, and user input rendering. For more information, see [Cross Site Scripting Prevention Cheat Sheet](Cross_Site_Scripting_Prevention_Cheat_Sheet.md).

**Path Traversal:**

Check for unsafe file path construction and directory traversal vulnerabilities. For more information, see [File Upload Cheat Sheet](File_Upload_Cheat_Sheet.md).

**Command Injection:**

Identify direct command execution with user input and unsafe system calls. For more information, see [OS Command Injection Defense Cheat Sheet](OS_Command_Injection_Defense_Cheat_Sheet.md).

**NoSQL Injection:**

Examine NoSQL query construction and parameter binding. For more information, see [NoSQL Security Cheat Sheet](NoSQL_Security_Cheat_Sheet.md).

### Authentication & Session Management Vulnerabilities

Review authentication mechanisms, session token generation, and user credential handling. For more information, refer to [Authentication Cheat Sheet](Authentication_Cheat_Sheet.md) and [Session Management Cheat Sheet](Session_Management_Cheat_Sheet.md).

### Access Control Vulnerabilities

Examine authorization checks, role-based access controls, and privilege escalation prevention. For more information, see [Authorization Cheat Sheet](Authorization_Cheat_Sheet.md).

### Deserialization Vulnerabilities

**Insecure Deserialization:**

Check for unsafe deserialization of untrusted data and object injection vulnerabilities. For more information, see [Deserialization Cheat Sheet](Deserialization_Cheat_Sheet.md).

**XML External Entity (XXE):**

Review XML parsing configurations and external entity processing. For more information, see [XML External Entity Prevention Cheat Sheet](XML_External_Entity_Prevention_Cheat_Sheet.md).

### Cryptographic Implementation Flaws

Examine encryption algorithms, key management, and cryptographic implementations. For more information, refer to [Cryptographic Storage Cheat Sheet](Cryptographic_Storage_Cheat_Sheet.md).

## Review Techniques

### Code Pattern Analysis

Focus on high-risk code patterns:

- Input processing and validation functions
- Database query construction and ORM usage
- File operations and path handling
- Authentication and session management logic
- Authorization and access control checks
- Cryptographic operations and key management
- Error handling and logging mechanisms
- Configuration loading and environment variables

### Data Flow Analysis

Trace data through the application:

1. **Identify Sources**: User inputs, file uploads, API calls, database reads, environment variables
2. **Follow Processing**: Validation, transformation, business logic, caching
3. **Check Sinks**: Database queries, file writes, output rendering, logging, external APIs
4. **Validate Boundaries**: Input validation and output encoding at trust boundaries
5. **Trust Zones**: Verify security controls at each trust boundary crossing
6. **Data Classification**: Ensure sensitive data receives appropriate protection

### Threat-Based Review

Align review with common attack patterns:

- **OWASP Top 10**: Focus on prevalent web application risks
- **STRIDE Model**: Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation
- **Attack Trees**: Map potential attack paths through the application
- **Abuse Cases**: Consider how features could be misused by attackers
- **Security Controls**: Verify defense-in-depth implementation

### Business Logic Review

Use the [Abuse Case Cheat Sheet](Abuse_Case_Cheat_Sheet.md) to identify misuse scenarios.

Analyze application workflows for:

- State management and transition validation
- Race conditions and concurrency issues
- Transaction integrity and rollback mechanisms
- Resource limits and quota enforcement
- Authorization at each workflow step
- Workflow bypass opportunities

## Review Checklists

### Input Validation

- [ ] **Server-side validation**: All inputs validated on server regardless of client-side checks
- [ ] **Allowlist validation**: Uses allowlists rather than blocklists for input validation
- [ ] **Output encoding**: Context-appropriate encoding (HTML, JavaScript, CSS, URL)
- [ ] **File upload security**: Content-based validation, size limits, safe storage
- [ ] **SQL injection prevention**: [Parameterized queries or safely implemented stored procedures](SQL_Injection_Prevention_Cheat_Sheet.md#primary-defenses) used, with user-controlled data values passed as parameters instead of concatenated into SQL
- [ ] **Length limits**: Input length restrictions enforced
- [ ] **Character handling**: Special characters and Unicode properly processed
- [ ] **Error messages**: No sensitive information disclosed in error responses

### Authentication & Session Management

- [ ] **Password security**: Strong hashing algorithms and salt usage (for more information, see [Password Storage Cheat Sheet](Password_Storage_Cheat_Sheet.md))
- [ ] **Account protection**: Lockout mechanisms with appropriate thresholds
- [ ] **Session management**: Secure token generation (≥128 bits entropy)
- [ ] **Session lifecycle**: Proper invalidation on logout/timeout
- [ ] **Re-authentication**: Required for sensitive operations
- [ ] **Multi-factor authentication**: Implementation for high-risk accounts (for more information, see [Multifactor Authentication Cheat Sheet](Multifactor_Authentication_Cheat_Sheet.md))
- [ ] **Password reset**: Secure, time-limited reset mechanisms (for more information, see [Forgot Password Cheat Sheet](Forgot_Password_Cheat_Sheet.md))
- [ ] **Session security**: HttpOnly, Secure, SameSite cookie attributes
- [ ] **Concurrent sessions**: Appropriate limits and monitoring

### Authorization

- [ ] **Server-side enforcement**: All access controls enforced server-side
- [ ] **Fail-safe defaults**: Default deny access policy
- [ ] **IDOR prevention**: Proper authorization for resource access (see [Insecure Direct Object Reference Prevention Cheat Sheet](Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.md))
- [ ] **Function-level controls**: Administrative functions properly protected
- [ ] **Role validation**: Role assignments cannot be manipulated
- [ ] **Privilege escalation**: Horizontal and vertical escalation prevented
- [ ] **Centralized decisions**: Access control logic centralized
- [ ] **Post-authentication checks**: Authorization verified after authentication

### Cryptography

- [ ] **Strong algorithms**: Modern algorithms (AES-256, RSA-2048+, ECDSA P-256+)
- [ ] **Key management**: Proper key generation, storage, and rotation (for more information, see [Key Management Cheat Sheet](Key_Management_Cheat_Sheet.md))
- [ ] **Certificate validation**: Proper validation including hostname verification
- [ ] **Random generation**: Cryptographically secure random number generation
- [ ] **Data protection**: Encryption at rest and in transit
- [ ] **IV/Nonce handling**: Follow the selected mode's requirements for initialization vectors (IVs) and nonces. For example, [cipher block chaining (CBC) requires unpredictable IVs](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf#page=27), while [Galois/Counter Mode (GCM) requires IV uniqueness under each key](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf#page=26) and permits deterministic generation
- [ ] **Library maintenance**: Up-to-date cryptographic libraries
- [ ] **Side-channel protection**: Consideration of timing and other side-channel attacks

### Business Logic

- [ ] **Workflow integrity**: Proper state validation in multi-step processes
- [ ] **Race condition prevention**: Synchronization in concurrent operations
- [ ] **Transaction atomicity**: Proper rollback and consistency mechanisms
- [ ] **Resource limits**: Rate limiting and resource quotas implemented (see [Denial of Service Cheat Sheet](Denial_of_Service_Cheat_Sheet.md))
- [ ] **Business rule enforcement**: Cannot bypass rules through direct API access

### Configuration & Deployment

- [ ] **Secure defaults**: Security-focused default configurations
- [ ] **Environment separation**: Proper isolation between environments
- [ ] **Secrets management**: No hardcoded secrets, proper secret storage and rotation (for more information, see [Secrets Management Cheat Sheet](Secrets_Management_Cheat_Sheet.md))
- [ ] **Error handling**: Graceful error handling without information disclosure (for more information, see [Error Handling Cheat Sheet](Error_Handling_Cheat_Sheet.md))
- [ ] **Logging security**: Sensitive data not logged, proper log protection (for more information, see [Logging Cheat Sheet](Logging_Cheat_Sheet.md))
- [ ] **Security headers**: Appropriate HTTP security headers configured (for more information, see [HTTP Headers Cheat Sheet](HTTP_Headers_Cheat_Sheet.md))
- [ ] **TLS configuration**: Strong cipher suites and protocol versions (for more information, see [Transport Layer Security Cheat Sheet](Transport_Layer_Security_Cheat_Sheet.md))
- [ ] **Dependency management**: Up-to-date libraries without known vulnerabilities (for more information, see [Vulnerable Dependency Management Cheat Sheet](Vulnerable_Dependency_Management_Cheat_Sheet.md))

### Security Monitoring

- [ ] **Security events**: Authentication failures, authorization violations logged
- [ ] **Anomaly detection**: Unusual patterns and behaviors monitored
- [ ] **Audit trails**: Complete audit logs for sensitive operations
- [ ] **Real-time alerts**: Critical security events trigger immediate notifications
- [ ] **Log integrity**: Logs protected from tampering and unauthorized access
- [ ] **Incident response**: Clear procedures for security incident handling

## Tools and Techniques

### Code Editors

Use editors with security extensions:

- Visual Studio Code with ESLint, SonarLint
- IntelliJ IDEA with SpotBugs, SonarLint
- Eclipse with security plugins
- Vim/Neovim with security linters

### Command-Line Pattern Detection

```bash
# Find hardcoded secrets
grep -ri "password\s*=\|api_key\s*=\|secret\s*=" source/

# Find unsafe functions
grep -r "eval(\|exec(\|innerHTML\|document\.write" source/

# Find potential injections
grep -r "SELECT.*+\|executeQuery.*+" source/
```

### Manual Review Focus Areas

**Human Expertise Advantages:**

- **Business Logic Flaws**: Complex workflows and state management issues that require domain understanding
- **Context-Specific Vulnerabilities**: Security issues that depend on application-specific business rules
- **Authorization Logic**: Complex permission models and access control implementations
- **Race Conditions**: Timing-based vulnerabilities in concurrent operations
- **Cryptographic Misuse**: Proper implementation of cryptographic primitives and protocols
- **Architecture Security**: High-level design flaws and security anti-patterns

**Manual Analysis Techniques:**

- **Code Path Tracing**: Following execution paths through complex business logic
- **State Analysis**: Understanding application state transitions and validation
- **Trust Boundary Mapping**: Identifying and analyzing security control points
- **Threat Modeling Integration**: Applying threat models to specific code implementations
- **Attack Scenario Simulation**: Mentally simulating attack paths through the code

### Automated Tool Integration

**Supporting Manual Reviews:**

- **SAST Tool Triage**: Use automated findings to prioritize manual review areas
- **Dependency Scanning**: Identify vulnerable libraries requiring manual assessment
- **Code Quality Metrics**: Focus manual effort on complex or frequently changed code
- **Pattern Detection**: Use tools to highlight potential security anti-patterns for human analysis

**Tool Integration Strategy:**

- **Pre-Review Scanning**: Run automated tools before manual review to identify obvious issues
- **Complementary Analysis**: Use tool findings to guide deeper manual investigation
- **False Positive Filtering**: Apply human judgment to validate automated findings
- **Coverage Gaps**: Focus manual review on areas automated tools cannot effectively analyze

**Security Metrics:**

- **Manual Review Coverage**: Percentage of critical code paths reviewed by humans
- **Finding Quality**: Ratio of valid security issues to total findings
- **Review Efficiency**: Time spent on manual review vs. security value delivered
- **Trend Analysis**: Security posture improvement over time

### Documentation Templates

**Finding Report Template:**

```text
Title: [Vulnerability Type] in [Component]
Severity: [Critical/High/Medium/Low]
CWE: [CWE Number and Name]
Location: [File:Line or Function]
Description: [Detailed explanation of the vulnerability]
Impact: [Security implications and potential attack scenarios]
Reproduction: [Steps to reproduce or proof of concept]
Recommendation: [Specific fix guidance with code examples]
References: [CWE links, OWASP references, vendor documentation]
Status: [Open/In Progress/Fixed/Accepted Risk]
Assignee: [Developer responsible for fix]
Due Date: [Target fix date]
```

**Review Summary Template:**

```text
Review Summary
==============
Application: [Application Name]
Version: [Version/Commit Hash]
Reviewer(s): [Names]
Review Date: [Date]
Scope: [Files/Components Reviewed]

Findings Summary:
- Critical: [Count]
- High: [Count] 
- Medium: [Count]
- Low: [Count]
- Informational: [Count]

Key Recommendations:
1. [Priority recommendation]
2. [Priority recommendation]
3. [Priority recommendation]

Overall Risk Assessment: [Low/Medium/High/Critical]
```

## Integration with SDLC

### Review Timing

#### Baseline Review Integration

- **Project Initiation**: Comprehensive security assessment of existing codebase
- **Major Releases**: Full security review before significant version releases
- **Architecture Changes**: Complete review when fundamental design changes occur
- **Compliance Cycles**: Periodic comprehensive reviews for regulatory requirements
- **Security Incidents**: Thorough review following security breaches or major vulnerabilities
- **Onboarding Legacy Systems**: Initial security assessment when bringing existing applications under secure development practices

#### Diff-Based Review Integration

- **Pull Requests**: Security-focused review of code changes as part of standard PR process
- **Pre-commit Hooks**: Lightweight security checks on developer commits
- **Feature Completion**: Security review of completed user stories or features
- **Sprint Reviews**: Regular assessment of security implications of sprint deliverables
- **Hotfix Reviews**: Rapid security assessment of emergency fixes
- **Continuous Integration**: Automated triggering of security reviews based on code changes

#### Hybrid Approach

- **Risk-Based Scheduling**: Combine baseline reviews for high-risk components with diff-based reviews for routine changes
- **Incremental Baseline Updates**: Gradually expand baseline review coverage over multiple development cycles
- **Trigger-Based Reviews**: Escalate from diff-based to baseline review when significant security concerns are identified

For CI/CD integration and automated security testing, for more information see [CI CD Security Cheat Sheet](CI_CD_Security_Cheat_Sheet.md).

### Team Collaboration

**Roles:**

- **Security reviewers**: Conduct analysis and provide guidance
- **Developers**: Implement fixes and follow secure coding practices
- **Security champions**: Bridge security and development teams

**Best Practices:**

- Use standardized checklists and templates
- Maintain a knowledge base of common issues
- Track metrics on review effectiveness
- Provide regular security training
- Integrate with existing development workflows

## Advanced Techniques

### Race Condition Analysis

Focus on Time-of-Check vs Time-of-Use (TOCTOU) vulnerabilities and ensure atomic operations.

### Business Logic Analysis

Analyze workflows for:

- State transitions and validation
- Opportunities to bypass steps or validation
- Proper validation at each workflow step
- Rollback mechanisms and cleanup on failures
- Behavior under concurrent access
- Boundary conditions and error scenarios

### Security Architecture Review

Review architecture patterns for consistent security enforcement and proper API security controls; see the [Secure Product Design Cheat Sheet](Secure_Product_Design_Cheat_Sheet.md).

### Memory Safety

Review buffer management, integer overflow protection, and resource limits.

## References

- [OWASP Code Review Guide, Version 2](https://raw.githubusercontent.com/OWASP/www-project-code-review-guide/master/assets/OWASP_Code_Review_Guide_v2.pdf)
- [NIST SP 800-218: Secure Software Development Framework (SSDF) Version 1.1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)

---

## Section 18: Sql Injection Prevention Cheat Sheet

# SQL Injection Prevention Cheat Sheet

## Introduction

This cheat sheet will help you prevent SQL injection flaws in your applications. It will define what SQL injection is, explain where those flaws occur, and provide four options for defending against SQL injection attacks. [SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection) attacks are common because:

1. SQL Injection vulnerabilities are very common.
2. The application's database is a frequent target for attackers because it typically contains sensitive or critical data.

## What Is a SQL Injection Attack?

Attackers can use SQL injection on an application if it has dynamic database queries that use string concatenation and user-supplied input. To avoid SQL injection flaws, developers need to:

1. Stop writing dynamic queries with string concatenation.
2. Prevent malicious SQL input from being included in executed queries.

There are simple techniques for preventing SQL injection vulnerabilities, and they can be used with practically any kind of programming language and any type of database. While XML databases can have similar problems (e.g., XPath and XQuery injection), these techniques can be used to protect them as well.

## Anatomy of a Typical SQL Injection Vulnerability

A common SQL injection flaw in Java is shown below. Because its unvalidated "customerName" parameter is simply appended to the query, an attacker can enter SQL code into that query and the application would take the attacker's code and execute it on the database.

```java
String query = "SELECT account_balance FROM user_data WHERE user_name = "
             + request.getParameter("customerName");
try {
    Statement statement = connection.createStatement( ... );
    ResultSet results = statement.executeQuery( query );
}

...
```

## Primary Defenses

- **Option 1: Use of Prepared Statements (with Parameterized Queries)**
- **Option 2: Use of Properly Constructed Stored Procedures**
- **Option 3: Allow-list Input Validation**
- **Option 4: STRONGLY DISCOURAGED: Escaping All User Supplied Input**

### Defense Option 1: Prepared Statements (with Parameterized Queries)

When developers are taught how to write database queries, they should be told to use prepared statements with variable binding (aka parameterized queries). Prepared statements are simple to write and easier to understand than dynamic queries, and parameterized queries force the developer to define all SQL code first and pass in each parameter to the query later.

If database queries use this coding style, the database will always distinguish between code and data, regardless of what user input is supplied. Also, prepared statements ensure that an attacker cannot change the intent of a query, even if SQL commands are inserted by an attacker.

#### Safe Java Prepared Statement Example

In the safe Java example below, if an attacker were to enter the userID as `tom' or '1'='1`, the parameterized query would look for a username that literally matches the entire string `tom' or '1'='1`. Thus, the database would be protected against injections of malicious SQL code.

The following code example uses a `PreparedStatement`, Java's implementation of a parameterized query, to execute the same database query.

```java
// This should REALLY be validated too
String custname = request.getParameter("customerName");
// Perform input validation to detect attacks
String query = "SELECT account_balance FROM user_data WHERE user_name = ? ";
PreparedStatement pstmt = connection.prepareStatement( query );
pstmt.setString( 1, custname);
ResultSet results = pstmt.executeQuery( );
```

#### Safe C\# .NET Prepared Statement Example

In .NET, the creation and execution of the query doesn't change. Just pass the parameters to the query using the `Parameters.Add()` call as shown below.

```csharp
String query = "SELECT account_balance FROM user_data WHERE user_name = ?";
try {
  OleDbCommand command = new OleDbCommand(query, connection);
  command.Parameters.Add(new OleDbParameter("customerName", CustomerName.Text));
  OleDbDataReader reader = command.ExecuteReader();
  // …
} catch (OleDbException se) {
  // error handling
}
```

While we have shown examples in Java and .NET, practically all other languages (including Cold Fusion and Classic ASP) support parameterized query interfaces. Even SQL abstraction layers, like the [Hibernate Query Language](http://hibernate.org/) (HQL) with the same type of injection problems (called [HQL Injection](http://cwe.mitre.org/data/definitions/564.html))  support parameterized queries as well:

#### Hibernate Query Language (HQL) Prepared Statement (Named Parameters) Example

```java
// This is an unsafe HQL statement
Query unsafeHQLQuery = session.createQuery("from Inventory where productID='"+userSuppliedParameter+"'");
// Here is a safe version of the same query using named parameters
Query safeHQLQuery = session.createQuery("from Inventory where productID=:productid");
safeHQLQuery.setParameter("productid", userSuppliedParameter);
```

#### Other Examples of Safe Prepared Statements

If you need examples of prepared queries/parameterized languages, including Ruby, PHP, Cold Fusion, Perl, and Rust, see the [Query Parameterization Cheat Sheet](Query_Parameterization_Cheat_Sheet.md) or this [site](http://bobby-tables.com/).

Generally, developers like prepared statements because all the SQL code stays within the application, which makes applications relatively database independent.

### Defense Option 2: Stored Procedures

Though stored procedures are not always safe from SQL injection, developers can use certain standard stored procedure programming constructs. This approach has the same effect as using parameterized queries, as long as the stored procedures are implemented safely (which is the norm for most stored procedure languages).

#### Safe Approach to Stored Procedures

If stored procedures are needed, the safest approach to using them requires the developer to build SQL statements with parameters that are automatically parameterized, unless the developer does something largely out of the norm. The difference between prepared statements and stored procedures is that the SQL code for a stored procedure is defined and stored in the database itself, then called from the application. Since prepared statements and safe stored procedures are equally effective in preventing SQL injection, your organization should choose the approach that makes the most sense for you.

#### When Stored Procedures Can Increase Risk

Occasionally, stored procedures can increase risk when a system is attacked. For example, on MS SQL Server, you have three main default roles: `db_datareader`, `db_datawriter` and `db_owner`. Before stored procedures came into use, DBAs would give `db_datareader` or `db_datawriter` rights to the webservice's user, depending on the requirements.

However, stored procedures require execute rights, a role not available by default. In some setups where user management has been centralized, but is limited to those 3 roles, web apps would have to run as `db_owner` so stored procedures could work. Naturally, that means that if a server is breached, the attacker has full rights to the database, where previously, they might only have had read-access.

#### Safe Java Stored Procedure Example

The following code example uses Java's implementation of the stored procedure interface (`CallableStatement`) to execute the same database query. The `sp_getAccountBalance` stored procedure has to be predefined in the database and use the same functionality as the query above.

```java
// This should REALLY be validated
String custname = request.getParameter("customerName");
try {
  CallableStatement cs = connection.prepareCall("{call sp_getAccountBalance(?)}");
  cs.setString(1, custname);
  ResultSet results = cs.executeQuery();
  // … result set handling
} catch (SQLException se) {
  // … logging and error handling
}
```

#### Safe VB .NET Stored Procedure Example

The following code example uses a `SqlCommand`, .NET's implementation of the stored procedure interface, to execute the same database query. The `sp_getAccountBalance` stored procedure must be predefined in the database and use the same functionality as the query defined above.

```vbnet
 Try
   Dim command As SqlCommand = new SqlCommand("sp_getAccountBalance", connection)
   command.CommandType = CommandType.StoredProcedure
   command.Parameters.Add(new SqlParameter("@CustomerName", CustomerName.Text))
   Dim reader As SqlDataReader = command.ExecuteReader()
   '...
 Catch se As SqlException
   'error handling
 End Try
```

### Defense Option 3: Allow-list Input Validation

If you are faced with parts of SQL queries that can't use bind variables, such as table names, column names, or sort order indicators (ASC or DESC), input validation or query redesign is the most appropriate defense. When table or column names are needed, ideally those values come from the code and not from user parameters.

#### Sample Of Safe Table Name Validation

WARNING: Using user parameter values to target table or column names is a symptom of poor design and a full rewrite should be considered if time allows. If that is not possible, developers should map the parameter values to the legal/expected table or column names to make sure unvalidated user input doesn't end up in the query.

In the example below, since `tableName` is identified as one of the legal and expected values for a table name in this query, it can be directly appended to the SQL query. Keep in mind that generic table validation functions can lead to data loss if table names are used in queries where they are not expected.

```text
String tableName;
switch(PARAM):
  case "Value1": tableName = "fooTable";
                 break;
  case "Value2": tableName = "barTable";
                 break;
  ...
  default      : throw new InputValidationException("unexpected value provided"
                                                  + " for table name");
```

#### Safest Use Of Dynamic SQL Generation (DISCOURAGED)

When we say a stored procedure is "implemented safely," that means it does not include any unsafe dynamic SQL generation. Developers do not usually generate dynamic SQL inside stored procedures. However, it can be done, but should be avoided.

If it can't be avoided, the stored procedure must use input validation or proper escaping, as described in this article, to make sure that all user supplied input to the stored procedure can't be used to inject SQL code into the dynamically generated query. Auditors should always look for uses of `sp_execute`, `execute` or `exec` within SQL Server stored procedures. Similar audit guidelines are necessary for similar functions for other vendors.

#### Sample of Safer Dynamic Query Generation (DISCOURAGED)

For something simple like a sort order, it is best if the user supplied input is converted to a boolean, and then that boolean is used to select the safe value to append to the query. This is a very standard need in dynamic query creation.

For example:

```java
public String someMethod(boolean sortOrder) {
 String SQLquery = "some SQL ... order by Salary " + (sortOrder ? "ASC" : "DESC");
 ...
```

Any time user input can be converted to a non-String, like a date, numeric, boolean, enumerated type, etc. before it is appended to a query, or used to select a value to append to the query, this ensures it is safe to do so.

Input validation is also recommended as a secondary defense in ALL cases, even when using bind variables as discussed earlier in this article. More techniques on how to implement strong input validation techniquies are described in the [Input Validation Cheat Sheet](Input_Validation_Cheat_Sheet.md).

### Defense Option 4: STRONGLY DISCOURAGED: Escaping All User-Supplied Input

In this approach, the developer will escape all user input before putting it in a query. It is very database specific in its implementation.  This methodology is fragile compared to other defenses, and we CANNOT guarantee that this option will prevent all SQL injections in all situations.

If an application is built from scratch or requires low risk tolerance, it should be built or re-written using parameterized queries, stored procedures, or some kind of Object Relational Mapper (ORM) that builds your queries for you.

## Additional Defenses

Beyond adopting one of the four primary defenses, we also recommend adopting all of these additional defenses to provide defense in depth. These additional defenses are:

- **Least Privilege**
- **Allow-list Input Validation**

### Least Privilege

To minimize the potential damage of a successful SQL injection attack, you should minimize the privileges assigned to every database account in your environment. Start from the ground up to determine what access rights your application accounts require, rather than trying to figure out what access rights you need to take away.

Make sure that accounts that only need read access are only granted read access to the tables they need access to. DO NOT ASSIGN DBA OR ADMIN TYPE ACCESS TO YOUR APPLICATION ACCOUNTS. We understand that this is easy, and everything just "works" when you do it this way, but it is very dangerous.

#### Minimizing Application and OS Privileges

SQL injection is not the only threat to your database data. Attackers can simply change the parameter values from one of the legal values they are presented with, to a value that is unauthorized for them, but the application itself might be authorized to access. As such, minimizing the privileges granted to your application will reduce the likelihood of such unauthorized access attempts, even when an attacker is not trying to use SQL injection as part of their exploit.

While you are at it, you should minimize the privileges of the operating system account that the DBMS runs under. Don't run your DBMS as root or system! Most DBMSs run out of the box with a very powerful system account. For example, MySQL runs as system on Windows by default! Change the DBMS's OS account to something more appropriate, with restricted privileges.

#### Details Of Least Privilege When Developing

If an account only needs access to portions of a table, consider creating a view that limits access to that portion of the data and assigning the account access to the view instead of the underlying table. Rarely, if ever, grant create or delete access to database accounts.

If you adopt a policy where you use stored procedures everywhere, and don't allow application accounts to directly execute their own queries, then restrict those accounts to only be able to execute the stored procedures they need. Don't grant them any rights directly to the tables in the database.

#### Least Admin Privileges For Multiple DBs

The designers of web applications should avoid using the same owner/admin account in the web applications to connect to the database. Different DB users should be used for different web applications.

In general, each separate web application that requires access to the database should have a designated database user account that the application will use to connect to the DB. That way, the designer of the application can have good granularity in the access control, thus reducing the privileges as much as possible. Each DB user will then have select access to only what it needs, and write-access as needed.

As an example, a login page requires read access to the username and password fields of a table, but no write access of any form (no insert, update, or delete). However, the sign-up page certainly requires insert privilege to that table; this restriction can only be enforced if these web apps use different DB users to connect to the database.

#### Enhancing Least Privilege with SQL Views

You can use SQL views to further increase the granularity of access by limiting the read access to specific fields of a table or joins of tables. It could have additional benefits.

For example, a product catalog can use a view that exposes product names and retail prices while omitting supplier costs. Grant the application's database account only `SELECT` access to that view, without access to the underlying table or other objects that expose the omitted fields. Verify your database's view privilege rules; for example, [PostgreSQL normally checks underlying table access using the view owner's privileges](https://www.postgresql.org/docs/current/sql-createview.html).

This limits the data exposed through a compromised application account. Queries against views still require parameterization to prevent SQL injection.

### Allow-list Input Validation

In addition to being a primary defense when nothing else is possible (e.g., when a bind variable isn't legal), input validation can also be a secondary defense used to detect unauthorized input before it is passed to the SQL query. For more information please see the [Input Validation Cheat Sheet](Input_Validation_Cheat_Sheet.md). Proceed with caution here. Validated data is not necessarily safe to insert into SQL queries via string building.

## Related Articles

See the [Query Parameterization Cheat Sheet](Query_Parameterization_Cheat_Sheet.md) for language-specific examples of prepared statements and stored procedures.

## References

- [Oracle JDBC: Using Prepared Statements](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html)
- [PHP PDO: Prepared Statements and Stored Procedures](https://www.php.net/pdo.prepared-statements)

---

