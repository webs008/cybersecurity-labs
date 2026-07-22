Overview

Before conducting an authorized penetration test or security audit, the penetration testing team and the client must establish clear boundaries for the engagement. This process is known as pre-engagement planning and involves defining what will be tested, how testing will be performed, when testing may occur, and how sensitive information will be handled.

The primary purpose of this process is to ensure that the penetration test is authorized, controlled, safe, and aligned with the client's objectives. A well-defined scope and Rules of Engagement (RoE) protect both the client and the penetration testing team from accidental disruption, unauthorized access, legal issues, and misunderstandings.
1. What Is Penetration Testing Scope?

The scope defines the systems, networks, applications, and environments that the penetration testing team is authorized to assess. The scope may include domains, subdomains, IP addresses, network ranges, servers, workstations, web applications, APIs, databases, cloud infrastructure, wireless networks, VPN infrastructure, physical locations, and user accounts.

A professional scope should also explicitly identify out-of-scope assets. For example, an organization may authorize testing of its own web application but exclude third-party infrastructure, cloud services owned by another organization, production databases, critical business systems, partner networks, or customer-facing infrastructure.

The scope should be specific enough that the testing team can determine whether a discovered asset is authorized for testing.
2. Why Scoping Is Important

Poorly defined scopes can create significant risks. A tester might accidentally attack an unauthorized system, test a third-party service, disrupt production, modify or delete business data, trigger an incident response process, affect customers, cause a denial of service, or violate contractual or legal requirements.

For example, during reconnaissance, a tester may discover an IP address that appears to belong to the target organization but is actually hosted by a third-party provider. The tester should not automatically assume that the system is authorized for testing. The correct approach is to:

    Identify the asset
    Determine ownership
    Compare it with the approved scope
    Request clarification if necessary
    Do not test it until authorization is confirmed

3. Rules of Engagement

The Rules of Engagement define the operational rules that govern how the penetration test will be conducted. The RoE should clearly answer who is authorized to test, what systems may be tested, where testing will originate, when testing can occur, what techniques are allowed, what techniques are prohibited, who should be contacted during an emergency, and how sensitive data should be handled.

The RoE is particularly important when testing production environments.
4. Authorization

Before testing begins, the penetration testing team should obtain formal authorization. The authorization should identify the client organization, authorized testing team, scope, testing period, approved techniques, approved targets, authorized source networks, and emergency contacts.

Common supporting documents may include a Statement of Work (SoW), Scope of Work, Rules of Engagement, Authorization to Test, Non-Disclosure Agreement (NDA), and Data Processing Agreement where applicable.

The key principle is: Never begin penetration testing without clear authorization.
5. Identifying the Client's Security Concerns

The penetration test should be aligned with the client's actual security objectives. During the initial interview, ask about the organization's biggest security concerns, whether they have experienced a security incident, if ransomware or data theft is a concern, if business disruption is a concern, if there are compliance requirements, and if privilege escalation or social engineering attacks are concerns.

For example, an online retailer may be particularly concerned about ransomware affecting warehouse operations, unauthorized access to inventory systems, compromise of employee accounts, privilege escalation, database compromise, or business interruption. These concerns should influence the testing methodology and priorities.
6. Identifying Systems and Networks in Scope

The scope should clearly identify the authorized targets. For network scope, document IP addresses, CIDR ranges, VLANs, VPN networks, DMZ networks, internal networks, and external networks. For infrastructure, document servers, workstations, firewalls, VPN gateways, network devices, databases, and cloud infrastructure. For applications, document web applications, APIs, mobile applications, authentication services, databases, and internal applications.

The more specific the scope, the lower the risk of accidental testing outside authorization.
7. Identifying Out-of-Scope Assets

Every engagement should explicitly define what must not be tested. Examples include third-party infrastructure, partner systems, customer systems, cloud resources owned by another organization, critical production systems, specific databases, network ranges, and wireless networks.

For example, an organization may use a third-party cloud provider to host part of its business infrastructure. The client's application may be in scope, while the underlying cloud provider infrastructure is out of scope. This distinction is critical.
8. Production vs Test Environment

The penetration testing team should determine whether testing will target production, staging, development, QA, or sandbox environments. If production testing is authorized, the Rules of Engagement should identify activities that may cause disruption.
Testing Activity	Production	Test Environment
Passive reconnaissance	Usually allowed	Allowed
Vulnerability scanning	Usually allowed with limits	Allowed
Authentication testing	With authorization	Allowed
Exploitation	Controlled	Preferred where possible
Load testing	Restricted	Preferred
DoS testing	Highly restricted	Preferred

Where possible, potentially disruptive tests should be performed against a test environment that accurately represents production.
9. Internal Network Testing

Internal penetration testing evaluates the security of systems that are accessible from inside the organization's network. The test may assess whether a compromised employee workstation could lead to privilege escalation, lateral movement, unauthorized server access, access to sensitive databases, or domain compromise.

The Rules of Engagement should document how internal access will be obtained. Possible methods include an isolated VLAN, VPN, jump host, bastion host, dedicated testing workstation, or on-site access. The source IP address or network range should be documented.
10. End-User Systems

End-user systems may be included when the objective is to determine whether a compromised employee account or workstation can be used to access critical systems. The scope should specify the number of users, departments, user accounts, workstations, and operating systems.

For example, an assessment may focus on warehouse employees to determine whether compromising a warehouse workstation could lead to unauthorized access to internal servers.
11. Social Engineering

Social engineering must be explicitly authorized. Possible activities include phishing simulations, spear phishing, vishing, smishing, and physical social engineering. The RoE should specify target employees, number of targets, approved email addresses, approved domains, testing period, permitted techniques, and prohibited techniques.

The client should also specify whether employees are aware of the testing. A realistic assessment may intentionally limit awareness to a small group of authorized personnel.
12. Denial-of-Service and Disruptive Testing

Denial-of-Service testing can cause significant operational impact and therefore requires explicit authorization. The RoE should define whether DoS testing is allowed, whether load testing is allowed, target systems, maximum intensity, maximum duration, approved time windows, monitoring procedures, and emergency stop procedures.

For example, an organization may permit disruptive testing only during a scheduled maintenance window, such as 02:00–06:00 on Friday, Saturday, and Sunday. Non-disruptive testing could then occur during normal business hours.
13. Security Controls That May Affect Testing

Security controls can detect, block, or modify penetration testing activity. Examples include firewalls, IDS, IPS, Web Application Firewalls, Endpoint Detection and Response, Security Information and Event Management systems, VPN controls, network segmentation, rate limiting, and endpoint security.

The testing team should document these controls because they may influence the results. For example, if a firewall blocks a test request, the tester should distinguish between "The application is secure" and "The firewall prevented the test from reaching the application." These are not the same conclusion.
14. Wireless Testing

Wireless testing should be explicitly defined. If included, document wireless networks, SSIDs, locations, access points, guest networks, and corporate networks. If wireless testing is not explicitly authorized, it should be treated as out of scope.
15. Web Services and APIs

The scope should identify whether web applications and APIs are included. Document URLs, domains, API endpoints, authentication systems, and supporting infrastructure. Testing should be limited to the authorized assets.

For example, an organization may authorize testing of its own e-commerce application but exclude third-party services integrated with that application.
16. Testing Awareness

The client should define who knows about the penetration test. Possible approaches include white-box (extensive information provided), gray-box (limited information provided), or black-box (minimal information provided). The RoE should document who knows about the test, who does not know, which security teams are informed, and whether employees are informed. This is particularly important for social engineering engagements.
17. Testing Timeline

The testing schedule should be clearly documented. Include contract signing, NDA signing, kickoff meeting, testing start date, testing end date, maintenance windows, reporting deadlines, and retesting dates.

For example, testing begins two weeks after contract and NDA execution, disruptive testing occurs only during approved maintenance windows, and the final report is delivered within 60 days.
18. Testing Location

Document where testing will originate. This may include a client office, data center, remote location, VPN, or isolated VLAN. Also document source IP address, source network, VPN gateway, and testing workstation.
19. Communication Plan

The communication plan should identify primary contacts, technical contacts, emergency contacts, reporting frequency, communication channels, and escalation procedures. For example, weekly progress reports,
