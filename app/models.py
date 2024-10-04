from django.db import models

class Empresa(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nome

class Departamento(models.Model):
    nome = models.CharField(max_length=255)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nome} - {self.empresa.nome}"

class Funcionario(models.Model):
    nome = models.CharField(max_length=255)
    rg = models.CharField(max_length=12, unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    rg = models.CharField(max_length=12, unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    
    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nome

class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)
    data_venda = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Venda {self.id} - {self.cliente.nome}"

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome} (Venda {self.venda.id})"

class Documento(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    tipo_documento = models.CharField(max_length=255)
    conteudo = models.TextField()
    data_emissao = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tipo_documento} - {self.data_emissao}"

class NotaFiscal(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    numero = models.CharField(max_length=20, unique=True)
    serie = models.CharField(max_length=20)
    data_emissao = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"NF {self.numero} - {self.venda.cliente.nome}"

class Pagamento(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateField()

    def __str__(self):
        return f"Pagamento {self.id} - {self.venda.cliente.nome}"
