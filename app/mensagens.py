# Dicionário com as mensagens personalizadas de cada transportadora
# Edite conforme sua necessidade

MENSAGENS_TRANSPORTADORAS = {
    "RODONAVES": "Seu pedido será entregue pela Transportadora *Rodonaves* para fazer o seu rastreio você deve acessar o site: https://rodonaves.com.br/rastreio-de-mercadoria, selecionar a opção *Nota fiscal* e então digitar seu *CPF ou CNPJ* e o numero da sua NF que é: *@NF@*",
    "JAMEF": "Seu pedido será entregue pela Transportadora *Jamef* para fazer o seu rastreio você deve acessar o site: https://jamef.com.br/#rastrear-carga, digitar o numero da sua NF: *@NF@* e o seu *CPF ou CNPJ*",
    "FLYVILLE": "Seu pedido será entregue pela Transportadora *Flyville* para fazer o seu rastreio você deve acessar o site: https://flyville.net.br/localize-sua-carga, digitar o numero da sua NF: @NF@ e o nosso *CNPJ* que é: *@DOCLOJA@*",
}

def get_mensagem(transportadora: str, num_nf, doc_cliente, doc_loja) -> str:
    """
    Retorna a mensagem personalizada para a transportadora informada.
    Caso não exista, retorna uma mensagem padrão.
    """

    return MENSAGENS_TRANSPORTADORAS.get(
        transportadora.split(' ')[0],
        "Sua entrega será realizada pela transportadora informada na nota fiscal."
    ).replace("@NF@", num_nf).replace("@DOCLOJA@", doc_loja).replace("@DOCCLIENTE@", doc_cliente)
