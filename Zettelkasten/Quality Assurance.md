As systems have become more complex, malfunctions, cost overruns, and missed deadlines are becoming more common, resulting in a need for more effective quality control processes. System quality control goes beyond debugging to include improving procedures and developing training for employees. The ISO 9000 series of standards address industrial activities such as design, production, installation, and servicing. The ISO/IEC 15504 is a set of standards developed jointly by the International Organization for Standardization (ISO) and the International Electrotechnical Commission (IEC). It is common for third-party system developers to meet specific standards.

Quality control must also maintain effective documentation practices. It is important that each step of the development process is accurately documented for future reference. Without maintaining up-to-date documentation, it is likely the records will be inaccurate or no longer applicable. Documenting the various audits throughout the [[system development process]] helps reduce errors.
### Testing

In the past, _**testing**_ was primarily the process of checking systems and confirming that the final product was compatible with the system requirement specification. Now, testing is only one part of quality assurance. Systems are not the only artifacts that are tested during the [[system development process]]. The result of each intermediate step in the entire development process is also tested for accuracy. Many system engineers believe that testing should be incorporated into the other steps of the development process, creating a three-step development process:

1. Requirements analysis and confirmation
2. Design and validation
3. Implementation and testing

Unfortunately, even with modern quality assurance techniques, large systems continue to contain errors. Even after significant testing periods, many errors go undetected for the life of the system, while other errors cause major malfunctions. Reducing these errors is one of the goals of system engineering.

Systems need thorough testing to ensure that functionality and performance requirements are met. System engineers have developed testing methodologies to improve the ability to identify errors with a limited number of tests. The Pareto principle is based on the theory that 80% of errors come from 20% of the system, meaning most errors can be identified by testing carefully selected groups of samples. Basis path testing is another [[software]] testing methodology. Basis path testing develops a set of test [[data]] that ensures each instruction in the [[software]] is executed at least once.

Techniques based on the Pareto principle and basis path testing rely on knowledge of a system's internal components. This is known as glass-box testing, commonly referred to as white-box testing, which includes having developers test internal structures of [[software]]. Black-box testing does not rely on the tester's knowledge of the system's structure but is focused on the user experience (UX).

Methodologies that fall within the black-box category are alpha, beta, and user acceptance testing. In alpha testing, the first stage, developers and/or an internal UX team test a preliminary version of the [[software]], providing feedback about performance and functionality. The second stage is beta testing, sometimes referred to as pilot testing. In this stage, the next version of the system is given to a segment of end users for similar testing from their perspective before the final version is released. The final stage is referred to as user acceptance testing. During this stage, the users test the system in an operational setting to make sure the system continues to align with business objectives and meet the goals of the stakeholders.
### Documentation

A system is not effective unless people can learn to use it and maintain it properly. Documentation is an important part of a system. The production of documentation is a component of the [[system development process]]. There are three types of system documentation: user documentation, system documentation, and technical documentation. User documentation explains the system to users and may include [[information]] such as how to access certain features, frequently asked questions (FAQs), and contact [[information]] for customer support.

System documentation describes the system's internal configuration so the system can be maintained later in its life cycle. A major part of [[software]] development system documentation is [[software]] code. The code needs to be versioned and presented in a readable format. Versioned code allows developers to track modifications and reverse any changes that have been problematic. Readability is important so that any contributing developer can read the code. Development companies have created conventions for writing programs that include several common features:

- indentation conventions for script readability
- naming conventions for variables and constraints
- documentation conventions for sufficient program documentation

Technical documentation describes how to install and maintain the system, including [[information]] about installing updates and providing feedback to the development team.