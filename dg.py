from diagrams import Diagram, Cluster
from diagrams.aws.compute import EKS
from diagrams.aws.network import VPC, InternetGateway, RouteTable, PublicSubnet, PrivateSubnet, NATGateway
from diagrams.aws.security import IAM
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.network import Service
from diagrams.aws.general import Users

with Diagram("EKS Cluster Architecture", show=False, direction="TB"):
    users = Users("Users")
    
    with Cluster("AWS Cloud"):
        # IAM 설정
        iam = IAM("IAM Roles")
        
        with Cluster("VPC"):
            # VPC 컴포넌트
            vpc = VPC("VPC")
            igw = InternetGateway("Internet Gateway")
            rt = RouteTable("Route Tables")
            
            # 서브넷 구성
            with Cluster("Availability Zone 1"):
                pub_subnet1 = PublicSubnet("Public Subnet 1")
                priv_subnet1 = PrivateSubnet("Private Subnet 1")
                nat1 = NATGateway("NAT Gateway 1")
                
            with Cluster("Availability Zone 2"):
                pub_subnet2 = PublicSubnet("Public Subnet 2")
                priv_subnet2 = PrivateSubnet("Private Subnet 2")
                nat2 = NATGateway("NAT Gateway 2")
            
            # EKS 클러스터
            with Cluster("EKS Cluster"):
                eks = EKS("EKS Control Plane")
                
                with Cluster("Worker Nodes"):
                    with Cluster("Node Group 1"):
                        pods1 = [Pod("Pod 1"), Pod("Pod 2")]
                        
                    with Cluster("Node Group 2"):
                        pods2 = [Pod("Pod 3"), Pod("Pod 4")]
                        
                    # 서비스 및 디플로이먼트
                    svc = Service("K8s Service")
                    deploy = Deployment("Deployment")

    # 연결 관계 정의
    users >> igw >> pub_subnet1
    igw >> pub_subnet2
    
    pub_subnet1 >> nat1 >> priv_subnet1
    pub_subnet2 >> nat2 >> priv_subnet2
    
    vpc >> rt
    
    eks >> iam
    eks >> pods1
    eks >> pods2
    
    for pod in pods1 + pods2:
        pod >> svc
        deploy >> pod
