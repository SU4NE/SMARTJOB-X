import csv
import sys

def obter_optimum_ou_lb(caminho_csv, instancia_alvo):
    with open(caminho_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for linha in reader:
            if linha['name'] == instancia_alvo:
                jobs = int(linha['jobs'])
                machines = int(linha['machines'])
                optimum = linha.get('optimum', '').strip()

                if optimum:
                    print(f"✅ Optimum da instância '{instancia_alvo}': {optimum}")
                else:
                    print(f"❌ Não há solução conhecida para '{instancia_alvo}'.")
                return

        print(f"❌ Instância '{instancia_alvo}' não encontrada no CSV.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"\n❌ Uso incorreto.")
        print(f"👉 Formato correto: python optimum.py <nome_da_instancia>\n")
        print(f"🔍 Exemplo: python optimum.py abz5")
        sys.exit(1)

    instancia_alvo = sys.argv[1].strip()

    if not instancia_alvo:
        print("⚠️ Nome da instância não pode estar vazio.")
        sys.exit(1)

    obter_optimum_ou_lb("respostas.csv", instancia_alvo)
