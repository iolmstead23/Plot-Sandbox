[[Networks]] rely on protocols to govern communication. Without protocols, the computers in a [[Networks|network]] might try to transmit messages at the same time or fail to provide needed assistance to other machines. Using protocols, vendors are able to build products for [[networks|network]] applications that are compatible with products from other vendors.

### Methods of Process Communication

Interprocess communication allows the activities or processes on different computers within a [[networks|network]] to coordinate actions and complete tasks.

#### Client/Server Model

Description of Client-Server [[Networks|network]] diagramClient-Server [[Networks|Network]] diagram with computers connected together through a switch. In the diagram, the switch appears in the middle. Above the switch, from left to right, are a [[desktop]] [[computer]] labeled [[computer]] A, a server labeled directory server, a server labeled file server, and a [[computer]] labeled [[computer]] b. Below the switch, there are two additional computers ([[Computer]] C and [[Computer]] D, respectively) and two laptops (laptop A and laptop B, respectively). Blue curvy lines represent the cables connecting each of the devices to the switch.

The client/server model is a popular convention used for interprocess communication. The basic roles played by the processes are categorized as either a client making requests or a server satisfying client requests. An early application of the client/server model appeared in [[networks]] connecting clusters of offices with a single printer available to all computers. The printer (also known as the print server) is the server, and the machines are clients requesting printed documents. Early networking systems also used file servers that accepted requests for company [[data]] that were centrally stored.

#### Peer-to-Peer (P2P)

Peer-to-peer (P2P) is another model for interprocess communication. In this model, processers both request and provide service to each other. Instant messaging and interactive games played by users on multiple machines are both examples of the P2P model.

A new generation of P2P services arose to fill the void, expanding the range of sharable file types and further decentralizing [[networks]]. The Gnutella protocol operates without any centralized server and allows for numerous [[software]] clients to be used for access, which makes it nearly impossible to shut down. BitTorrent, used commonly for distributing large video files, employs a “swarm” model, whereby files are downloaded in simultaneous pieces from multiple host computers. Newer services have established degrees of [[encryption]] and anonymity to protect users from legal action by copyright holders.

#### Distributed Systems

Interactions between computers via [[networks]] have become commonplace and multifaceted. Many modern systems, such as global [[information]] retrieval systems or [[computer]] games, are designed as distributed systems. Distributed systems execute [[software]] as processes on more than one [[computer]].

There are several types of distributed systems. 

- Cluster computing uses many independent computers to provide computation or services comparable to those of a larger machine. The cost of several individual machines can be less than a higher-priced supercomputer, with comparable performance. Cluster computing provides high availability as it is likely that at least one [[computer]] in the cluster will be able to answer a request even when others in the cluster are unavailable or broken down. In addition, clusters can balance loads by automatically shifting requests among the cluster members.
- Grid computing is a type of distributed system that is more loosely coupled than clusters but still works together as a system to complete large tasks. Grid computing typically includes specialized [[software]] to make it easier to distribute the workload and [[data]] among the machines in the grid.
- Cloud computing provides large pools of shared computers that can be allocated to clients as needed. Services such as Amazon’s Elastic Compute Cloud allow clients to rent virtual computers by the hour no matter where the associated [[computer]] [[hardware]] is located. Services such as Google Cloud and Google Apps allow users to collaborate or build web services without needing to know how many computers are working on the problem or where the relevant [[data]] is stored. Cloud computing provides reasonable guarantees for reliability and scalability while raising concerns about security and privacy.