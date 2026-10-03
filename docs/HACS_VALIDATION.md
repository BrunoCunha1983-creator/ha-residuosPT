# Validação HACS

## Diagnóstico de 3 de outubro de 2026

O [run 37093447373](https://github.com/BrunoCunha1983-creator/ha-residuosPT/actions/runs/37093447373)
executou o job `validate-hacs` sobre o commit
`6ec49be464c0cf0c1a12acd26c95c6c9f5e6ab37` de `main`.
As cinco anotações correspondem a três causas, um resumo de falha e um aviso:

| Anotação | Nível | Significado e correção |
| --- | --- | --- |
| `The repository has no license` | failure | Adicionar uma licença reconhecida pelo GitHub à raiz da branch predefinida. Este conjunto de alterações propõe MIT. |
| `The repository has no description` | failure | Preencher a descrição em **About** no GitHub. |
| `The repository has no valid topics` | failure | Adicionar tópicos em **About** no GitHub. |
| `3/9 checks failed` | failure | Resumo das três falhas anteriores; não representa uma quarta causa. |
| `The ubuntu-latest label will migrate to Ubuntu 26 beginning October 19, 2026` | notice | Aviso do runner, sem relação com a reprovação HACS. O workflow passa a usar `ubuntu-24.04`, a mesma versão principal do runner do run analisado. |

Passaram as verificações `information`, `brands`, `issues`, `archived`,
`integration_manifest` e `hacsjson`.

## Metadados a configurar no GitHub

Estes campos pertencem ao repositório e não são configurados pelo README,
`hacs.json` ou `manifest.json`. A inclusão deste guia não os altera.

Na página principal do repositório, abrir a engrenagem de **About** e guardar:

- **Description:** `Integração Home Assistant para calendários semanais e sensores de recolha de resíduos em Portugal.`
- **Topics:** `home-assistant`, `hacs`, `custom-integration`, `waste-collection`, `recycling`, `portugal`.

Como alternativa, com GitHub CLI autenticado numa conta com permissão de edição:

```sh
gh repo edit BrunoCunha1983-creator/ha-residuosPT \
  --description 'Integração Home Assistant para calendários semanais e sensores de recolha de resíduos em Portugal.' \
  --add-topic home-assistant \
  --add-topic hacs \
  --add-topic custom-integration \
  --add-topic waste-collection \
  --add-topic recycling \
  --add-topic portugal
```

O comando adiciona os tópicos sem remover outros que já existam.

## Licença e verificação final

Rever a proposta de licença MIT e integrar as alterações em `main`.
O validador de licença HACS consulta os metadados do repositório devolvidos
pelo GitHub; um ficheiro `LICENSE` apenas na branch do PR pode continuar
a deixar esta verificação a falhar até ser integrado na branch predefinida.

Confirmar a descrição, os tópicos e a identificação SPDX da licença:

```sh
gh api repos/BrunoCunha1983-creator/ha-residuosPT \
  --jq '{description: .description, topics: .topics, license: .license.spdx_id}'
```

A licença deverá aparecer como `MIT`; a descrição e os tópicos deverão estar
preenchidos. Se o GitHub ainda não tiver reconhecido a licença, aguardar pela
atualização destes metadados antes de repetir a validação.

O push de integração em `main` inicia o workflow. Para iniciar uma execução
adicional após atualizar os metadados, usar **Actions > Validate > Run workflow > main**,
ou:

```sh
gh workflow run validate.yml --repo BrunoCunha1983-creator/ha-residuosPT --ref main
gh run list --repo BrunoCunha1983-creator/ha-residuosPT --workflow validate.yml --branch main --limit 5
```

Verificar que o novo run corresponde ao commit final e que `validate-hacs`
termina em `success`, com as nove verificações concluídas. Uma validação local
dos ficheiros não comprova os metadados nem substitui este resultado remoto.

O workflow mantém `hacs/action@main`, `category: integration` e `permissions: {}`.
Não são usados `ignore` nem `continue-on-error`.

## Referências

- [HACS Action](https://hacs.xyz/docs/publish/action/)
- [Validação da licença](https://github.com/hacs/integration/blob/adb7d83e33d24325535fb43b8226572405143757/custom_components/hacs/validate/license.py)
- [Validação da descrição](https://github.com/hacs/integration/blob/adb7d83e33d24325535fb43b8226572405143757/custom_components/hacs/validate/description.py)
- [Validação dos tópicos](https://github.com/hacs/integration/blob/adb7d83e33d24325535fb43b8226572405143757/custom_components/hacs/validate/topics.py)
