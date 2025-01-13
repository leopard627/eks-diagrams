from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EKS, ECS, Lambda
from diagrams.aws.network import Route53, ELB, VPC
from diagrams.aws.security import WAF, SecretsManager
from diagrams.aws.integration import Eventbridge, SQS
from diagrams.aws.database import ElastiCache, RDS
from diagrams.aws.storage import S3
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.onprem.database import MongoDB
from diagrams.generic.compute import Rack
from diagrams.generic.network import Firewall
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import Service, Ingress
from diagrams.programming.framework import Flask, React

# 다이어그램 스타일 설정
graph_attr = {
    "fontsize": "45",
    "bgcolor": "white",
    "splines": "ortho",
    "pad": "2.0",
}

with Diagram("Hybrid MultiAgent AI Architecture", 
             show=False, 
             direction="TB",
             graph_attr=graph_attr,
             filename="hybrid_multiagent_arch"):
    
    # 외부 클라이언트
    with Cluster("External Access"):
        dns = Route53("DNS")
        waf = WAF("WAF")
        alb = ELB("Application\nLoad Balancer")

    # AWS EKS 클러스터
    with Cluster("AWS Cloud - EKS Infrastructure"):
        with Cluster("VPC"):
            # EKS 컨트롤 플레인
            eks = EKS("EKS Control Plane")
            
            with Cluster("Kubernetes Workloads"):
                # API 및 오케스트레이션 레이어
                with Cluster("API & Orchestration Layer"):
                    api = Service("API Gateway")
                    ingress = Ingress("Ingress Controller")
                    orchestrator = Pod("AI Orchestrator")
                
                # 서비스 레이어
                with Cluster("Service Layer"):
                    services = [
                        Pod("Task Scheduler"),
                        Pod("Agent Manager"),
                        Pod("Model Registry")
                    ]
                
                # 경량 AI 에이전트
                with Cluster("Lightweight AI Agents"):
                    light_agents = [
                        Deploy("Routing Agent"),
                        Deploy("Planning Agent"),
                        Deploy("Memory Agent")
                    ]
            
            # AWS 서비스
            with Cluster("AWS Services"):
                queue = SQS("Message Queue")
                cache = ElastiCache("Redis Cache")
                secrets = SecretsManager("Secrets")
                events = Eventbridge("Event Bus")
                storage = S3("Model Storage")

    # 온프레미스 A100 인프라
    with Cluster("On-premises A100 Infrastructure"):
        firewall = Firewall("Security Gateway")
        
        with Cluster("Resource Management"):
            resource_manager = Nginx("Resource Manager")
            metrics = MongoDB("Metrics Store")
        
        with Cluster("GPU Farm"):
            gpu_servers = [Rack("A100 Server 1"),
                         Rack("A100 Server 2")]
            
            with Cluster("Heavy AI Models"):
                heavy_models = [
                    Pod("LLM Agent"),
                    Pod("Vision Agent"),
                    Pod("Speech Agent"),
                    Pod("Specialist Agent")
                ]

    # 연결 관계 정의
    # 외부 접근
    dns >> waf >> alb
    alb >> ingress
    
    # EKS 내부 연결
    ingress >> api >> orchestrator
    orchestrator >> services
    
    for service in services:
        service >> light_agents
        service >> events
    
    # AWS 서비스 연결
    events >> queue
    queue >> Edge(style="dashed") >> resource_manager
    orchestrator >> Edge(color="red") >> secrets
    light_agents[0] >> Edge(color="blue") >> cache
    
    # 온프레미스 연결
    resource_manager >> gpu_servers
    for server in gpu_servers:
        server >> heavy_models
    
    # 데이터 흐름
    heavy_models[0] >> Edge(color="green", style="bold") >> metrics
    metrics >> Edge(color="orange", style="dashed") >> events
    
    # 모델 스토리지 연결
    storage >> Edge(color="purple") >> heavy_models
    storage >> Edge(color="purple") >> light_agents
