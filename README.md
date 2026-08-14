# Recolha de Resíduos Portugal — Home Assistant

Integração customizada para Home Assistant orientada à recolha seletiva em Portugal.

## Entidades

- Próxima recolha — Amarelo (plástico/metal/embalagens)
- Próxima recolha — Azul (papel/cartão)
- Próxima recolha — Verde (vidro)
- Próxima recolha — Castanho (biorresíduos)
- Próxima recolha — Indiferenciado
- Próxima recolha geral
- Calendário nativo com todas as recolhas

Cada sensor inclui atributos com a cor do contentor, tipo de resíduo, dias configurados, operador, município e um guia básico do que colocar/não colocar.

## Instalação manual

Copie a pasta `custom_components/recolha_residuos_pt` para `/config/custom_components/recolha_residuos_pt` e reinicie o Home Assistant.

Depois vá a **Definições > Dispositivos e Serviços > Adicionar integração** e procure por **Recolha de Resíduos Portugal**.

## HACS

O repositório está estruturado para ser adicionado como repositório personalizado do tipo **Integration**.

## Como funciona nesta versão

A versão 0.1.0 usa um calendário semanal configurado pela interface. Isto torna a base independente do município e permite funcionar mesmo quando o operador só publica calendários em PDF/imagem.

A arquitetura foi preparada para evolução para adaptadores automáticos por operador/município.

## Cores principais usadas em Portugal

- Amarelo: embalagens de plástico e metal (incluindo pacotes de bebida)
- Azul: papel e cartão
- Verde: embalagens de vidro
- Castanho: biorresíduos, quando disponível localmente
- Cinzento/preto: indiferenciado (a cor física pode variar localmente)

Os calendários e métodos de recolha são locais e podem variar por município, freguesia/bairro e operador.
