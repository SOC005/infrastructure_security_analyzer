provider "aws" {
  region = "us-east-1"
}

# MISCONFIGURATION 1: RDS Database open to public
resource "aws_db_instance" "main_db" {
  identifier          = "prod-database"
  engine              = "mysql"
  instance_class      = "db.t3.micro"
  publicly_accessible = true        # INSECURE
  port                = 3306
  skip_final_snapshot = true
}

# MISCONFIGURATION 2: S3 Bucket open to everyone
resource "aws_s3_bucket" "data_bucket" {
  bucket = "prod-data-storage"
  acl    = "public-read-write"      # INSECURE
}

# MISCONFIGURATION 3: VM with no encryption
resource "aws_instance" "web_vm" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  root_block_device {
    encrypted = false               # INSECURE
  }
}

# MISCONFIGURATION 4: Container with all ports open
resource "aws_security_group" "container_sg" {
  name = "container-service-sg"
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]    # INSECURE
  }
}

# MISCONFIGURATION 5: Blob storage with public access
resource "azurerm_storage_blob" "app_blob" {
  name                   = "app-data"
  storage_account_name   = "prodstorageaccount"
  storage_container_name = "appcontainer"
  type                   = "Block"
  access_tier            = "public"  # INSECURE
}
