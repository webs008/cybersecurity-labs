# PortSwigger Web Security Academy Lab Write-up

# Lab Details

**Lab Name:** Excessive trust in client-side controls

**Category:** Business Logic Vulnerabilities

**Difficulty:** Practitioner

**Lab URL:** (https://portswigger.net/web-security/logic-flaws#what-are-business-logic-vulnerabilities)

**Date Completed:** (15/July/2026)

---

# Objective

The objective of this lab is to 
understand how business logic vulnerabilities arise when an application 
fails to correctly enforce its intended rules and workflows. The lab 
demonstrates how an attacker can manipulate legitimate application 
functionality by interacting with it in unexpected ways, causing the 
application to perform actions that were not intended by its developers.

---

# Background

## Vulnerability Overview

Business logic vulnerabilities are 
flaws in the design or implementation of an application's business 
rules. Rather than exploiting technical weaknesses such as SQL injection
 or Cross-Site Scripting (XSS), these vulnerabilities exploit incorrect 
assumptions about how users will interact with the application.

Unlike many traditional vulnerabilities, business logic flaws abuse legitimate functionality to produce unintended behavior.

### Definition

A business logic vulnerability is a 
weakness in the application's design or workflow that allows an attacker
 to manipulate normal functionality to achieve unauthorized or 
unintended results.

These vulnerabilities occur when the 
application fails to properly enforce the business rules governing 
transactions, workflows, permissions, or user interactions.

### Why It Occurs

Business logic vulnerabilities 
commonly arise because developers make assumptions about user behavior 
that are not enforced by the server.

Common causes include:

- Trusting client-side validation.
- Assuming users will follow the intended workflow.
- Missing or inadequate server-side validation.
- Poor handling of unexpected application states.
- Incomplete understanding of interactions between application components.
- Failure to document design assumptions.
- Complex application workflows introducing hidden logic flaws.

Because attackers can intercept and 
modify requests, they are not limited by the restrictions imposed by the
 application's user interface.

### Potential Impact

The severity of business logic vulnerabilities depends on the affected functionality.

Possible impacts include:

- Authentication bypass
- Privilege escalation
- Unauthorized access
- Business rule bypass
- Financial fraud
- Manipulation of transactions
- Unauthorized discounts
- Data integrity issues
- Increased attack surface
- Reputational damage
- Loss of customer trust

Even seemingly harmless logic flaws may later be combined with other weaknesses to produce high-severity attacks.

### Real-World Example (Optional)

An online shopping application 
calculates product prices using JavaScript in the browser. If the server
 accepts the client-supplied price without verifying it, an attacker 
could modify the request using Burp Suite and purchase products for an 
arbitrary amount.

---

# Prerequisites

Tools and knowledge required before starting the lab.

**Browser:**

- Firefox or Chrome

**Burp Suite:**

- Burp Suite Community or Professional
- Proxy configured to intercept browser traffic

**Other Tools:**

- Browser Developer Tools (optional)

**Required Knowledge:**

- HTTP Requests and Responses
- Client-side vs Server-side validation
- Business Logic concepts
- Burp Suite Proxy
- Request interception
- Parameter manipulation
- Basic web application architecture

---

# Lab Environment

**Target Application:**

PortSwigger Web Security Academy Lab

**Application URL:**

(https://portswigger.net/web-security/logic-flaws#what-are-business-logic-vulnerabilities)

**Authentication Required:**

Depends on the specific lab.

---

# Initial Reconnaissance

## Application Overview

The application provides normal web 
functionality that users are expected to interact with through a browser
 interface. Before testing, the application should be explored to 
understand its pages, workflows, transactions, forms, and business 
processes.

The objective during reconnaissance 
is to identify how the application expects users to behave before 
attempting to identify opportunities to deviate from that expected 
behavior.

---

## Pages Explored

- Home
- Login
- Product Pages
- Shopping Cart
- Checkout
- User Account
- Search
- Order History (if applicable)

---

## Interesting Features

- User authentication
- Shopping workflow
- Product purchasing
- Cart management
- Price calculations
- Client-side validation
- Promotional features
- Coupons or discounts (if present)

---

# Identifying the Vulnerability

## Initial Observation

The application contains 
functionality that relies on predefined business rules. During testing, 
attention is given to identifying areas where those rules appear to be 
enforced only by the browser or where unexpected user input may alter 
the application's behavior.

Indicators include:

- Hidden form fields
- JavaScript calculations
- Client-side validation
- Disabled controls
- Predictable workflows
- User-controlled parameters

---

## Evidence Collected

Evidence may include:

- HTTP requests
- HTTP responses
- Hidden parameters
- Modified requests
- Screenshots
- Unexpected server responses
- Successful manipulation of application behavior

---

# Exploitation Process

## Step 1

**Action Performed**

Explore the application and understand its intended workflow.

**Reason for the Action**

To establish normal application behavior.

**Result**

Normal workflow documented.

---

## Step 2

**Action Performed**

Intercept relevant HTTP requests using Burp Suite.

**Reason for the Action**

To inspect data transmitted between the browser and the server.

**Result**

Relevant requests identified.

---

## Step 3

**Action Performed**

Analyze request parameters and identify user-controlled values.

**Reason for the Action**

To determine whether security-critical values are supplied by the client.

**Result**

Potentially vulnerable parameters identified.

---

## Step 4

**Action Performed**

Modify one or more request parameters and resend the request.

**Reason for the Action**

To determine whether the server independently validates user input.

**Result**

Observe whether the server accepts or rejects the modified request.

---

## Step 5

**Action Performed**

Analyze the server's response and application behavior.

**Reason for the Action**

To confirm whether the business rule can be bypassed.

**Result**

Determine whether a business logic vulnerability exists.

---

# Burp Suite Analysis

## HTTP Request

Intercept the request responsible for the targeted functionality.

Record:

- HTTP Method
- Endpoint
- Parameters
- Cookies
- Headers

---

## Parameters Observed

| Parameter | Description | Notes |
| --- | --- | --- |
| Product ID | Identifies the selected product | User controlled |
| Quantity | Number of products | User controlled |
| Price | Transaction value | Verify whether validated server-side |

---

## Request Modifications

Document:

- Parameter modified
- Original value
- Modified value
- Reason for modification

---

## HTTP Response

Record:

- Status Code
- Response Body
- Error Messages
- Changes to application behavior
- Whether the modification was accepted

---

# Lab Solution

The application was tested by first 
observing its intended workflow and identifying how business rules were 
enforced. HTTP requests associated with the target functionality were 
intercepted using Burp Suite and inspected for user-controlled 
parameters. Selected values were modified and resent to determine 
whether the server independently validated the supplied data.

The application's response 
demonstrated whether it trusted client-controlled input or correctly 
enforced business rules on the server. Acceptance of manipulated values 
confirmed the presence of a business logic vulnerability.

---

# Root Cause

The vulnerability exists because the 
application makes incorrect assumptions about user behavior and fails to
 verify that those assumptions remain true when processing requests.

Typical root causes include:

- Excessive trust in client-side controls
- Missing server-side validation
- Poor workflow validation
- Inadequate state verification
- Failure to validate transaction-critical values

---

# Security Impact

If present in a production application, business logic vulnerabilities could lead to:

- Authentication bypass
- Privilege escalation
- Unauthorized transactions
- Financial fraud
- Manipulation of prices
- Abuse of discounts
- Business process manipulation
- Data integrity violations
- Increased attack surface

The overall impact depends on the business function affected.

---

# Remediation

Developers should:

- Perform all security-critical validation on the server.
- Never trust client-side controls.
- Validate every user-supplied value.
- Verify application state before processing requests.
- Enforce business rules server-side.
- Perform authorization checks for every request.
- Document assumptions within workflows.
- Review complex workflows during code reviews.
- Conduct manual business logic testing in addition to automated scans.

---

# Lessons Learned

### Technical Lessons

- Business logic flaws arise from incorrect assumptions rather than technical coding errors.
- Client-side validation should improve usability, not enforce security.
- Manual testing is essential for identifying logic flaws.

---

### Burp Suite Skills Practiced

- Proxy interception
- Request inspection
- Parameter manipulation
- Response analysis

---

### New Concepts Learned

- Business logic vulnerabilities
- Application workflow analysis
- Trust boundaries
- Server-side validation

---

# Key Takeaways

- Business logic vulnerabilities exploit flaws in application design rather than traditional technical weaknesses.
- Attackers often succeed by deviating from expected user behavior.
- Every security-critical business rule must be enforced on the server.
- Understanding application workflows is essential for identifying logic flaws.