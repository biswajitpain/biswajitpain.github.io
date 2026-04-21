# Biswajit Pain

- **Location:** Berlin, Germany
- **Phone:** +49 151 24865920
- **Email:** biswajit.pain[AT]outlook.com
- **GitHub:** [biswajitpain](https://github.com/biswajitpain)
- **LinkedIn:** [biswajitpain](https://www.linkedin.com/in/biswajitpain)

## Profile

Systems Development Engineer with 12+ years building and operating production cloud and distributed-storage infrastructure across AWS, Delivery Hero, Sixt, and VMware. Hands-on experience with Ceph (RBD, RGW, CephFS), Rook on Kubernetes, OpenStack (Cinder, Swift, Nova), and VMware vSAN / vSphere storage, delivered in both production and internal-platform environments. Day-to-day engineering in Go, Python, and Bash across AWS, GCP, and private datacenters; deep troubleshooting through Linux, networking, and the storage layer — from block device and filesystem behavior up to S3 / object gateway semantics.

## Professional Experience

### Amazon Web Services (AWS)
- **Position:** Lead Systems Development Engineer
- **Period:** October 2022 – Present
- **Location:** Berlin, Germany

**Database service — region build and storage layout**
- Owned the redesign of the region build process for a managed database service with a large distributed storage footprint, deployed across AWS regions.
- Rebuilt the provisioning pipeline so new regions come up with correct control-plane topology, storage layout, replication configuration, and networking without manual intervention.
- Shortened time-to-first-customer in a new region and removed a class of bootstrap failures caused by race conditions in the storage and control-plane initialization flow.

**Sovereign Cloud — Berlin engineering org**
- Part of the founding engineering group setting up AWS European Sovereign Cloud infrastructure in Berlin.
- Ran hundreds of technical interviews (systems design, coding, service deep-dive) to build the local engineering bench for a regulated, isolated cloud region.
- Contributed to early technical decisions on service isolation, operator access, and data-residency boundaries.

**Game orchestration platform**
- Engineer on the platform that orchestrates game server fleets for one of the largest game-hosting services on AWS.
- Worked on scheduling, capacity, and low-latency session placement across regions.

**Team & operations**
- Technical lead for 10 engineers split across Berlin and a second continent; own architecture reviews, design docs, and on-call quality for the team's services.

### Delivery Hero SE
- **Position:** Staff Systems Engineer
- **Period:** April 2020 – September 2022
- **Location:** Berlin, Germany

**Zero-downtime MySQL migration on GCP**
- Led migration of a large production MySQL estate to Google Cloud SQL for a globally used ordering platform.
- Designed the cutover using replication, read-only windows, and application-level dual-write verification so there was no visible downtime for restaurants or customers.
- Built pre- and post-migration consistency checks (row counts, checksum-based diff on critical tables) to prove correctness before committing to the new primary.

**Fintech payment reliability**
- Debugged and fixed recurring failures in the payment processing path: idempotency gaps, duplicate-charge edge cases, and timeouts against external PSPs.
- Added retry/backoff, circuit breakers, and clearer reconciliation jobs; cut payment-related incident volume and improved settlement accuracy.

**Internal tooling**
- Wrote internal CLIs and dashboards (Python + Grafana) to speed up incident triage across the distributed payment services.

### Sixt Research & Development
- **Position:** Manager III, Site Reliability Engineering
- **Period:** April 2018 – March 2020
- **Location:** Berlin / Munich, Germany

**Hydrant — infrastructure automation platform**
- Led Hydrant: an internal platform that automated provisioning of AWS accounts, VPCs, IAM baselines, and standard service stacks for product teams.
- Replaced hand-rolled tickets and ad-hoc Terraform usage with a self-service flow; cut new-environment setup from days to under an hour.
- Stack: Terraform, Python, Jenkins, AWS Organizations.

**PCI DSS–compliant payment platform on AWS**
- Designed and deployed the payment platform against PCI DSS requirements: network segmentation, restricted IAM, centralized logging, encryption at rest and in transit, audit trails.
- Drove the audit with external assessors and passed compliance on first attempt.

**Team leadership**
- Managed 7 SREs across Munich and Bangalore; ran hiring, on-call rotations, and roadmap planning across the two sites.

### VMware Software India Pvt. Ltd.
- **Position:** Member of Technical Staff II
- **Period:** November 2016 – March 2018
- **Location:** Bangalore, India

**Ceph storage for multi-cloud IaaS — production and internal**
- Designed and operated Ceph clusters providing block (RBD), object (RGW / S3-compatible), and file (CephFS) services backing the multi-cloud IaaS platform used by internal product teams and customer-facing workloads.
- Sized and built the CRUSH map and pool layout (replicated and erasure-coded pools, separate device classes for SSD and HDD tiers) to match durability and latency targets for different workload classes.
- Tuned BlueStore OSDs, placement group counts, scrub schedules, and recovery/backfill throttles to keep client IO predictable during node loss and rebalance events.
- Operated RGW for S3-compatible object storage: bucket lifecycle policies, user and quota management, and multi-site replication between sites.

**Rook operator on Kubernetes**
- Deployed and operated Rook to run Ceph on Kubernetes for internal platforms, automating cluster bring-up, OSD lifecycle on node churn, and version upgrades through the operator.
- Built StorageClasses and CSI bindings so product teams could consume RBD volumes and CephFS shares as first-class Kubernetes PersistentVolumes.
- Wrote runbooks and automation around the Rook CRDs (CephCluster, CephBlockPool, CephObjectStore) for day-2 operations: capacity expansion, pool changes, and failure recovery.

**OpenStack + Ceph integration**
- Integrated Ceph with OpenStack services — RBD as the backend for Cinder (block) and Glance (image), Swift-compatible object storage via RGW — so tenants got unified storage across compute, image, and object APIs.
- Worked across Nova, Cinder, Neutron, and Keystone to debug cross-component issues (volume attach races, auth token failures, network policy and QoS at the storage network layer).
- Reviewed tenant isolation, rate-limiting, and quota enforcement for multi-tenant shared storage.

**vSAN and vSphere storage**
- Ran vSAN clusters and vSphere storage policies in parallel with the Ceph environments; compared vSAN-based and Ceph-based backends on performance, operational cost, and failure modes to guide platform direction.

**Platform engineering — microservices and CI**
- Broke out services from a large monolithic test/CI system into independently deployable microservices with clear API boundaries; introduced service-level health checks and per-service deployment pipelines.

### ANI Technologies (Ola)
- **Position:** Production Engineer
- **Period:** January 2016 – October 2016
- **Location:** Bangalore, India

**HAProxy log analytics pipeline**
- Built the HAProxy log pipeline using rsyslog, Kafka, Logstash, and Elasticsearch for real-time visibility into traffic patterns and error rates across the fleet.
- Used the pipeline to identify slow upstreams and misbehaving clients that had previously been invisible.

**Microservice infrastructure**
- Contributed to the platform supporting the company's rapid user growth: service discovery, deploy tooling, and base images.

### Knowlarity
- **Position:** DevOps Engineer
- **Period:** April 2014 – December 2015
- **Location:** Bangalore, India

**Multi-datacenter VoIP telephony infrastructure**
- Designed and built the multi-datacenter VoIP telephony infrastructure powering the company's cloud telephony product across India and SEA.
- Built the active-active datacenter layout with SIP trunk termination across sites, media server pools, and carrier-level redundancy so call traffic survived single-DC loss.
- Owned the failover platform end-to-end: DNS, load balancer, Asterisk/FreeSWITCH media nodes, and DB replica cutover runbooks.

**Complex hub-and-spoke network**
- Designed and rolled out a hub-and-spoke network connecting multiple datacenters, office sites, and carrier interconnects with redundant IPsec tunnels and dynamic routing.
- Replaced an unstable full-mesh VPN setup; resolved persistent inter-site routing loops, asymmetric paths, and fragmentation issues that had been causing dropped calls and signaling failures.
- Tuned OSPF/BGP route preferences and failover timers so spoke sites re-converged on the surviving hub within seconds of a link loss.

### Tata Consultancy Services (TCS)
- **Position:** Assistant Systems Engineer / Trainee
- **Period:** July 2013 – March 2014
- **Location:** Kolkata, India
- **Achievements:**
  - Delivered infrastructure automation work including storage virtualization tasks for a client engagement.
  - Led a team of five during the Initial Learning Program.

## Technical Skills

- **Languages:** Go, Python, Bash, C, Java
- **Kubernetes & Containers:** Kubernetes, Helm, container runtimes, CRDs / operators, microservices
- **Cloud & IaaS:** AWS (EC2, S3, Route53, RDS, CloudFront, CloudWatch, SES, SNS, IAM), GCP, VMware IaaS
- **Ceph & Distributed Storage:** Ceph RBD, RGW, CephFS; Rook operator on Kubernetes; CRUSH maps, placement groups, BlueStore OSDs, erasure coding, replication factors, pool and bucket design; cluster recovery, scrub / backfill tuning, RGW multi-site
- **OpenStack:** Cinder (block), Swift (object), Nova (compute), Keystone, Neutron; Ceph-backed Cinder and Glance, OpenStack + Ceph integration patterns
- **Storage:** VMware vSAN, vSphere storage, enterprise storage (IBM, Hitachi), NAS, S3 / object storage, block volumes, replication, failover
- **Data:** MySQL, PostgreSQL, Kafka, Elasticsearch, data migration
- **Infra as Code / CI/CD:** Terraform, Chef, Puppet, Jenkins, Git-based pipelines
- **Observability:** OpenTSDB, Graylog, Fluentd, Logstash, rsyslog, cAdvisor, Nagios
- **OS / Networking:** Linux (RHEL, Ubuntu), performance tuning, TCP/IP, VPN (hub-and-spoke), HAProxy, load balancing
- **Web Frameworks:** Django, Flask

## Education

- **B.Tech, Computer Science and Engineering**
  - Institution: Kalyani Government Engineering College, India (2013)

_Last Updated: April 2026_
