#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template
import sys
import os
import time
from datetime import datetime

# Garante que o Python consiga encontrar o script dentro da subpasta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'emerg-automação')))
from spir_automatico_total import SPIRAutomatico

app = Flask(__name__, template_folder='.')

# Variável global para manter a sessão do navegador aberta entre os cliques
bot_global = None

@app.route('/')
def index():
    return render_template('emergencia.html')

@app.route('/abrir-navegador', methods=['GET', 'POST'])
def abrir_navegador():
    global bot_global
    print(f"⚡ Passo 1: Abrindo Chrome para login manual às {datetime.now()}...")
    
    try:
        # Se já tiver um navegador aberto por engano, fecha
        if bot_global and bot_global.driver:
            try: bot_global.driver.quit()
            except: pass
            
        bot_global = SPIRAutomatico()
        bot_global.configurar_chrome()
        bot_global.driver.get("https://spir.cpfl.com.br/")
        
        return jsonify({"sucesso": True, "mensagem": "Navegador aberto com sucesso!"})
    except Exception as e:
        print(f"❌ Erro ao abrir Chrome: {e}")
        return jsonify({"sucesso": False, "erro": str(e)})

@app.route('/executar-filtros', methods=['GET', 'POST'])
def executar_filtros():
    global bot_global
    print(f"⚡ Passo 2: Comando recebido! Disparando filtros IMEDIATAMENTE às {datetime.now()}...")
    
    if not bot_global or not bot_global.driver:
        return jsonify({"sucesso": False, "erro": "O navegador não está aberto. Clique em 'Buscar Dados SPIR' primeiro."})
        
    try:
        url_atual = bot_global.driver.current_url.lower()
        
        # Alerta amigável caso você clique sem estar na tela correta
        if "monitoram" not in url_atual:
            print("⚠️ Usuário clicou mas ainda não está na tela do Monitor AM. Forçando navegação...")
            bot_global.navegar_para_monitor()
            time.sleep(1.5)
            
        # 🤖 O robô executa os filtros instantaneamente sem nenhuma espera ou loop
        bot_global.configurar_filtros_automatico()
        capturou = bot_global.capturar_emergencias_total()
        
        if capturou:
            bot_global.salvar_dados()
            total_capturado = len(bot_global.emergencias)
            lista_emergencias = bot_global.emergencias
            
            # Fecha o navegador após o sucesso
            bot_global.driver.quit()
            bot_global = None
            
            return jsonify({
                "sucesso": True, 
                "total": total_capturado, 
                "emergencias": lista_emergencias,
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            })
        else:
            return jsonify({"sucesso": False, "erro": "Nenhuma emergência localizada na tabela do portal."})
            
    except Exception as e:
        print(f"❌ Erro durante a execução dos filtros: {e}")
        return jsonify({"sucesso": False, "erro": str(e)})

if __name__ == '__main__':
    print("🚀 Servidor de Integração por Cliques ativo!")
    print("👉 Acesse o painel por aqui: http://127.0.0.1:5000")
    app.run(port=5000, debug=False)