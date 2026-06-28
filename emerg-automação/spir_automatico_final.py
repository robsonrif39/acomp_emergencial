"""
SPIR Automático - Versão Final com Filtros Específicos
Captura automática de emergências do SPIR com filtros precisos:
- Período: Últimos 15 dias
- Estação Avançada OM: APENAS Americana
- Estados: Aguardando Análise, Concluído, Aguardando Execução, Execução
"""

import time
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class SPIRAutomaticoFinal:
    def __init__(self):
        self.driver = None
        self.dados_emergencias = []
        
    def configurar_chrome(self):
        """Configura o Chrome para automação"""
        print("🔧 Configurando Chrome...")
        
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Configurar Chrome automaticamente
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Remover indicadores de automação
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Chrome configurado com sucesso!")
        
    def fazer_login_com_assistencia(self, usuario, senha):
        """Faz login no SPIR com assistência manual quando necessário"""
        print("🔐 Fazendo login no SPIR...")
        
        try:
            # Acessar página de login
            self.driver.get("https://spir.cpfl.com.br/")
            
            # Aguardar carregamento
            wait = WebDriverWait(self.driver, 30)
            time.sleep(3)
            
            # Tentar login automático primeiro
            print("   🤖 Tentando login automático...")
            
            # Encontrar campos de login
            usuario_seletores = [
                "input[name='username']", "input[name='user']", "input[name='login']",
                "input[type='text']", "input[id*='user']"
            ]
            
            senha_seletores = [
                "input[name='password']", "input[name='senha']", "input[type='password']"
            ]
            
            # Encontrar campo usuário
            campo_usuario = None
            for seletor in usuario_seletores:
                try:
                    campo_usuario = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor)))
                    print(f"   ✅ Campo usuário encontrado: {seletor}")
                    break
                except:
                    continue
            
            # Encontrar campo senha
            campo_senha = None
            for seletor in senha_seletores:
                try:
                    campo_senha = self.driver.find_element(By.CSS_SELECTOR, seletor)
                    print(f"   ✅ Campo senha encontrado: {seletor}")
                    break
                except:
                    continue
            
            # Se encontrou os campos, tentar preenchimento automático
            if campo_usuario and campo_senha:
                try:
                    print("   📝 Preenchendo credenciais automaticamente...")
                    
                    campo_usuario.clear()
                    campo_usuario.send_keys(usuario)
                    
                    campo_senha.clear()
                    campo_senha.send_keys(senha)
                    
                    # Procurar botão de login
                    botao_login = None
                    botao_seletores = [
                        "button[type='submit']", "input[type='submit']",
                        "button[class*='login']", "button[class*='entrar']"
                    ]
                    
                    for seletor in botao_seletores:
                        try:
                            botao_login = self.driver.find_element(By.CSS_SELECTOR, seletor)
                            break
                        except:
                            continue
                    
                    if botao_login:
                        botao_login.click()
                    else:
                        campo_senha.send_keys(Keys.RETURN)
                    
                    print("   ⏳ Verificando resultado do login automático...")
                    time.sleep(5)
                    
                    # Verificar se login deu certo
                    url_atual = self.driver.current_url
                    if "login" not in url_atual.lower() and "account" not in url_atual.lower():
                        print("   ✅ Login automático bem-sucedido!")
                        return True
                    
                except Exception as e:
                    print(f"   ❌ Erro no login automático: {e}")
            
            # Se chegou aqui, login automático falhou - ativar modo manual
            print("   🔴 Login automático falhou - ATIVANDO MODO MANUAL")
            
        except Exception as e:
            print(f"   ❌ Erro na tentativa automática: {e}")
        
        # MODO MANUAL
        print("\n" + "=" * 80)
        print("🔴 MODO MANUAL ATIVADO - FAÇA LOGIN MANUALMENTE:")
        print(f"   👤 Usuário sugerido: {usuario}")
        print("   🔑 Digite a senha correta no navegador")
        print("   🖱️ Clique em 'Entrar' ou 'Login'")
        print("   ⏳ Aguarde até sair da tela de login")
        print("   ✅ Pressione ENTER aqui quando login estiver completo")
        print("=" * 80)
        
        # Aguardar intervenção manual
        input("\n👆 PRESSIONE ENTER APÓS FAZER LOGIN MANUAL: ")
        
        return True
    
    def selecionar_empresa_paulista_assistido(self):
        """Seleciona empresa Paulista com assistência manual"""
        print("\n🏢 Selecionando empresa Paulista...")
        
        try:
            wait = WebDriverWait(self.driver, 15)
            time.sleep(3)
            
            # Verificar se há uma tela de seleção de empresa
            url_atual = self.driver.current_url
            print(f"   📍 URL atual: {url_atual}")
            
            # Procurar por elementos que indicam seleção de empresa
            indicadores_empresa = [
                "Selecione o grupo de empresas",
                "Grupo/Empresa de acesso", 
                "CPFL ENERGIA",
                "Paulista"
            ]
            
            tem_selecao_empresa = False
            for indicador in indicadores_empresa:
                try:
                    if self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{indicador}')]"):
                        tem_selecao_empresa = True
                        print(f"   ✅ Tela de seleção detectada: '{indicador}'")
                        break
                except:
                    continue
            
            if not tem_selecao_empresa:
                print("   ℹ️ Não foi detectada tela de seleção de empresa")
                print("   ✅ Continuando para próxima etapa...")
                return True
            
            # Tentar seleção automática primeiro
            print("   🤖 Tentando seleção automática de Paulista...")
            
            paulista_selecionado = False
            
            # ESTRATÉGIA 1: Select tradicional
            try:
                selects = self.driver.find_elements(By.TAG_NAME, "select")
                for select_elem in selects:
                    select_obj = Select(select_elem)
                    for opcao in select_obj.options:
                        if "paulista" in opcao.text.lower():
                            select_obj.select_by_visible_text(opcao.text)
                            print(f"   ✅ Paulista selecionado automaticamente: '{opcao.text}'")
                            paulista_selecionado = True
                            break
                    if paulista_selecionado:
                        break
            except Exception as e:
                print(f"   ❌ Erro na estratégia 1: {e}")
            
            # ESTRATÉGIA 2: Elementos clicáveis
            if not paulista_selecionado:
                try:
                    elementos_paulista = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Paulista')]")
                    for elem in elementos_paulista:
                        if elem.is_displayed() and elem.is_enabled():
                            elem.click()
                            print("   ✅ Paulista clicado automaticamente")
                            paulista_selecionado = True
                            break
                except Exception as e:
                    print(f"   ❌ Erro na estratégia 2: {e}")
            
            # Se seleção automática falhou, ativar modo manual
            if not paulista_selecionado:
                print("   🔴 Seleção automática falhou - MODO MANUAL")
                print("\n" + "=" * 70)
                print("🔴 SELECIONE A EMPRESA PAULISTA MANUALMENTE:")
                print("   🎯 Procure por 'Paulista' na lista de empresas")
                print("   🖱️ Clique em 'Paulista'")
                print("   🖱️ Clique no botão 'OK'")
                print("   ✅ Pressione ENTER aqui quando terminar")
                print("=" * 70)
                
                input("\n👆 PRESSIONE ENTER APÓS SELECIONAR PAULISTA: ")
                print("   ✅ Seleção manual concluída!")
            else:
                # Procurar botão OK
                print("   🔍 Procurando botão OK...")
                
                # Procurar botão OK
                botao_ok_encontrado = False
                botao_seletores = [
                    "button[type='submit']", "input[type='submit']",
                    "//button[contains(text(), 'OK')]", "//input[@value='OK']"
                ]
                
                for seletor in botao_seletores:
                    try:
                        if seletor.startswith("//"):
                            botoes = self.driver.find_elements(By.XPATH, seletor)
                        else:
                            botoes = self.driver.find_elements(By.CSS_SELECTOR, seletor)
                        
                        for botao in botoes:
                            if botao.is_displayed() and botao.is_enabled():
                                botao.click()
                                print("   ✅ Botão OK clicado!")
                                botao_ok_encontrado = True
                                break
                        
                        if botao_ok_encontrado:
                            break
                    except:
                        continue
                
                if not botao_ok_encontrado:
                    print("   ⚠️ Botão OK não encontrado - tentando ENTER")
                    try:
                        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.RETURN)
                    except:
                        pass
            
            # Aguardar redirecionamento
            print("   ⏳ Aguardando redirecionamento...")
            time.sleep(5)
            
            return True
            
        except Exception as e:
            print(f"   ❌ Erro na seleção de empresa: {e}")
            return True  # Continuar mesmo com erro
    
    def navegar_para_monitor(self):
        """Navega para Monitor AM - ACESSO DIRETO"""
        print("\n🗺️ Navegando DIRETAMENTE para Monitor AM...")
        
        try:
            # Acesso direto ao Monitor AM
            url_monitor = "https://spir.cpfl.com.br/Consultas/MonitorAM/Visualizar"
            print(f"   🎯 Acessando: {url_monitor}")
            
            self.driver.get(url_monitor)
            time.sleep(5)
            
            # Verificar se foi redirecionado para login
            url_atual = self.driver.current_url
            print(f"   📍 URL atual: {url_atual}")
            
            if "login" in url_atual.lower() or "account" in url_atual.lower():
                print("   🔄 Redirecionado para login - fazendo login...")
                return False  # Indica que precisa fazer login
            else:
                print("   ✅ Monitor AM acessado diretamente!")
                return True
                
        except Exception as e:
            print(f"   ❌ Erro ao navegar para Monitor AM: {e}")
            return False
    
    def configurar_filtros_especificos(self):
        """Configura filtros específicos: Americana, últimos 15 dias, estados específicos"""
        print("\n🎯 Configurando filtros ESPECÍFICOS...")
        
        try:
            wait = WebDriverWait(self.driver, 20)
            time.sleep(5)  # Aguardar carregamento completo
            
            # 1. CONFIGURAR PERÍODO - Últimos 15 dias
            print("   📅 Configurando período (últimos 15 dias)...")
            
            data_fim = datetime.now()
            data_inicio = data_fim - timedelta(days=15)
            
            data_inicio_str = data_inicio.strftime("%d/%m/%Y")
            data_fim_str = data_fim.strftime("%d/%m/%Y")
            
            print(f"      📆 Período: {data_inicio_str} a {data_fim_str}")
            
            try:
                campos_data = self.driver.find_elements(By.CSS_SELECTOR, 
                    "input[type='text'][placeholder*='data'], input[type='date']")
                
                if len(campos_data) >= 2:
                    campos_data[0].clear()
                    campos_data[0].send_keys(data_inicio_str)
                    
                    campos_data[1].clear()
                    campos_data[1].send_keys(data_fim_str)
                    
                    print("      ✅ Período configurado automaticamente")
                else:
                    print("      ⚠️ Configure o período manualmente")
                    
            except Exception as e:
                print(f"      ❌ Erro na configuração de data: {e}")
            
            # 2. CONFIGURAR ESTAÇÃO AVANÇADA OM - APENAS AMERICANA
            print("   🏭 Configurando Estação Avançada OM (APENAS Americana)...")
            
            try:
                # PROCURAR ESPECIFICAMENTE PELO CAMPO "ESTAÇÃO AVANÇADA OM"
                campo_estacao = None
                
                # Estratégias para encontrar o campo
                seletores_estacao = [
                    "//label[contains(text(), 'Estação Avançada OM')]/following-sibling::select",
                    "//label[contains(text(), 'Estação Avançada OM')]/..//select",
                    "//*[contains(text(), 'Estação Avançada OM')]/following-sibling::*//select",
                    "//*[contains(text(), 'Estação Avançada OM')]/..//select",
                    "//select[contains(@id, 'EstacaoOM') or contains(@name, 'EstacaoOM')]",
                    "//select[contains(@class, 'estacao')]"
                ]
                
                for seletor in seletores_estacao:
                    try:
                        elementos = self.driver.find_elements(By.XPATH, seletor)
                        for elem in elementos:
                            if elem.is_displayed():
                                campo_estacao = elem
                                print(f"      ✅ Campo Estação Avançada OM encontrado!")
                                break
                        if campo_estacao:
                            break
                    except:
                        continue
                
                if campo_estacao:
                    select_obj = Select(campo_estacao)
                    
                    # Listar opções disponíveis
                    opcoes = [opt.text.strip() for opt in select_obj.options]
                    print(f"      📋 Opções disponíveis: {opcoes}")
                    
                    # PRIMEIRO: Desmarcar tudo (se for múltipla seleção)
                    try:
                        select_obj.deselect_all()
                        print("      ➖ Desmarcou todas as seleções")
                    except:
                        pass
                    
                    # SEGUNDO: Selecionar APENAS Americana
                    americana_encontrado = False
                    for opcao in select_obj.options:
                        if "americana" in opcao.text.lower():
                            select_obj.select_by_visible_text(opcao.text)
                            print(f"      ✅ AMERICANA SELECIONADO: '{opcao.text}'")
                            americana_encontrado = True
                            break
                    
                    if not americana_encontrado:
                        print("      ❌ Americana não encontrado nas opções!")
                        print("      🔴 CONFIGURAÇÃO MANUAL OBRIGATÓRIA!")
                        self._configuracao_manual_americana()
                    
                else:
                    print("      ❌ Campo Estação Avançada OM não encontrado!")
                    print("      🔴 CONFIGURAÇÃO MANUAL OBRIGATÓRIA!")
                    self._configuracao_manual_americana()
                
            except Exception as e:
                print(f"      ❌ Erro na configuração de Americana: {e}")
                self._configuracao_manual_americana()
            
            # 3. CONFIGURAR ESTADOS ESPECÍFICOS
            print("   📋 Configurando Estados específicos...")
            
            estados_desejados = [
                "Aguardando Análise",
                "Concluído", 
                "Aguardando Execução",
                "Execução"
            ]
            
            try:
                # Encontrar todos os checkboxes de estado
                checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
                
                estados_configurados = []
                
                for checkbox in checkboxes:
                    try:
                        # Encontrar texto associado
                        parent = checkbox.find_element(By.XPATH, "./..")
                        texto_estado = parent.text.strip()
                        
                        # Verificar se é um dos estados desejados
                        estado_desejado = False
                        for estado in estados_desejados:
                            if estado.lower() in texto_estado.lower():
                                if not checkbox.is_selected():
                                    checkbox.click()
                                    print(f"      ✅ Estado '{estado}' SELECIONADO")
                                else:
                                    print(f"      ✅ Estado '{estado}' já estava selecionado")
                                estados_configurados.append(estado)
                                estado_desejado = True
                                break
                        
                        # Se não é desejado e está marcado, desmarcar
                        if not estado_desejado and checkbox.is_selected() and texto_estado:
                            checkbox.click()
                            print(f"      ➖ Estado '{texto_estado}' DESMARCADO")
                        
                    except:
                        continue
                
                if estados_configurados:
                    print(f"      ✅ Estados configurados: {', '.join(estados_configurados)}")
                else:
                    print("      ⚠️ Configure os estados manualmente")
                    
            except Exception as e:
                print(f"      ❌ Erro na configuração de estados: {e}")
            
            # 4. EXECUTAR PESQUISA
            print("   🔍 Executando pesquisa...")
            
            try:
                botao_pesquisa = None
                seletores_pesquisa = [
                    "//button[contains(text(), 'PESQUISAR')]",
                    "//button[contains(text(), 'Pesquisar')]",
                    "//input[@value='PESQUISAR']",
                    "button[type='submit']"
                ]
                
                for seletor in seletores_pesquisa:
                    try:
                        if seletor.startswith("//"):
                            botoes = self.driver.find_elements(By.XPATH, seletor)
                        else:
                            botoes = self.driver.find_elements(By.CSS_SELECTOR, seletor)
                        
                        for botao in botoes:
                            if botao.is_displayed() and botao.is_enabled():
                                botao.click()
                                print("      ✅ Botão PESQUISAR clicado!")
                                botao_pesquisa = botao
                                break
                        
                        if botao_pesquisa:
                            break
                    except:
                        continue
                
                if botao_pesquisa:
                    print("      ⏳ Aguardando carregamento dos resultados...")
                    time.sleep(15)  # Aguardar mais tempo para carregar
                else:
                    print("      ⚠️ Botão PESQUISAR não encontrado")
                    print("      🔴 CLIQUE MANUALMENTE EM PESQUISAR e aguarde carregar")
                    input("      👆 PRESSIONE ENTER APÓS PESQUISAR: ")
                
            except Exception as e:
                print(f"      ❌ Erro ao executar pesquisa: {e}")
            
            print("   ✅ Configuração de filtros concluída!")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro geral na configuração: {e}")
            return False
    
    def _configuracao_manual_americana(self):
        """Solicita configuração manual de Americana"""
        print("\n" + "=" * 80)
        print("🔴 CONFIGURAÇÃO MANUAL OBRIGATÓRIA - ESTAÇÃO AVANÇADA OM:")
        print("   🎯 Encontre o campo 'Estação Avançada OM'")
        print("   ➖ DESMARQUE todas as outras estações")
        print("   ✅ MARQUE APENAS 'Americana'")
        print("   🔍 Clique em 'PESQUISAR'")
        print("   ⏳ Aguarde carregar os resultados")
        print("=" * 80)
        input("\n👆 PRESSIONE ENTER APÓS CONFIGURAR AMERICANA E PESQUISAR: ")
    
    def capturar_todas_emergencias(self):
        """Captura TODAS as emergências com estratégias múltiplas"""
        print("\n📊 Capturando TODAS as emergências...")
        
        try:
            wait = WebDriverWait(self.driver, 30)
            
            # Aguardar carregamento completo
            print("   ⏳ Aguardando carregamento completo...")
            time.sleep(10)
            
            # Verificar se há paginação
            print("   🔍 Verificando paginação...")
            
            elementos_paginacao = self.driver.find_elements(By.XPATH, 
                "//*[contains(text(), 'página') or contains(text(), 'Página') or contains(text(), 'registros')]")
            
            if elementos_paginacao:
                for elem in elementos_paginacao:
                    print(f"      📄 Info paginação: {elem.text}")
            
            # Tentar expandir todos os registros
            print("   🔍 Tentando mostrar todos os registros...")
            
            # Procurar select de quantidade de registros
            selects_qtd = self.driver.find_elements(By.CSS_SELECTOR, 
                "select[name*='length'], select[id*='length'], select option")
            
            for select_elem in selects_qtd:
                try:
                    if select_elem.tag_name == "select":
                        select_obj = Select(select_elem)
                        opcoes = [opt.text for opt in select_obj.options]
                        print(f"      📋 Opções quantidade: {opcoes}")
                        
                        # Tentar selecionar "Todos" ou maior número
                        for opcao in select_obj.options:
                            if "todos" in opcao.text.lower() or "all" in opcao.text.lower():
                                select_obj.select_by_visible_text(opcao.text)
                                print(f"      ✅ Selecionado: {opcao.text}")
                                time.sleep(5)
                                break
                        else:
                            # Se não tem "Todos", pegar o maior número
                            numeros = []
                            for opcao in select_obj.options:
                                try:
                                    num = int(opcao.text)
                                    numeros.append((num, opcao))
                                except:
                                    continue
                            
                            if numeros:
                                maior_num, maior_opcao = max(numeros)
                                select_obj.select_by_visible_text(maior_opcao.text)
                                print(f"      ✅ Selecionado maior: {maior_num}")
                                time.sleep(5)
                        break
                except:
                    continue
            
            # Scroll para carregar tudo
            print("   📜 Fazendo scroll completo...")
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            # Procurar tabela principal
            print("   🔍 Procurando tabela de dados...")
            
            tabelas = self.driver.find_elements(By.CSS_SELECTOR, "table")
            
            if not tabelas:
                print("   ❌ Nenhuma tabela encontrada!")
                return []
            
            # Escolher a tabela com mais linhas
            tabela_principal = max(tabelas, key=lambda t: len(t.find_elements(By.TAG_NAME, "tr")))
            linhas = tabela_principal.find_elements(By.TAG_NAME, "tr")
            
            print(f"   ✅ Tabela principal: {len(linhas)} linhas")
            
            # Extrair dados
            dados_emergencias = []
            cabecalho_detectado = False
            
            for i, linha in enumerate(linhas):
                try:
                    celulas = linha.find_elements(By.TAG_NAME, "td")
                    if not celulas:
                        celulas = linha.find_elements(By.TAG_NAME, "th")
                    
                    if len(celulas) < 3:
                        continue
                    
                    dados_linha = [celula.text.strip() for celula in celulas]
                    
                    # Detectar cabeçalho
                    if not cabecalho_detectado and i < 3:
                        texto_linha = " ".join(dados_linha).lower()
                        if any(palavra in texto_linha for palavra in ["evento", "am", "município", "data", "status"]):
                            print(f"      📋 Cabeçalho detectado: {dados_linha[:3]}")
                            cabecalho_detectado = True
                            continue
                    
                    # Verificar se tem dados válidos
                    if not any(dados_linha):
                        continue
                    
                    # Criar objeto emergência
                    emergencia = {
                        "id": len(dados_emergencias) + 1,
                        "am": dados_linha[0] if len(dados_linha) > 0 else "",
                        "evento": dados_linha[1] if len(dados_linha) > 1 else "",
                        "inicio": dados_linha[2] if len(dados_linha) > 2 else "",
                        "previsao": dados_linha[3] if len(dados_linha) > 3 else "",
                        "municipio": dados_linha[4] if len(dados_linha) > 4 else "",
                        "equipamento": dados_linha[5] if len(dados_linha) > 5 else "",
                        "causa": dados_linha[6] if len(dados_linha) > 6 else "",
                        "status": dados_linha[7] if len(dados_linha) > 7 else "",
                        "dados_completos": dados_linha,
                        "capturado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "filtros": {
                            "periodo": "Últimos 15 dias",
                            "estacao_om": "Americana",
                            "estados": ["Aguardando Análise", "Concluído", "Aguardando Execução", "Execução"]
                        }
                    }
                    
                    # Só adicionar se tem dados mínimos
                    if emergencia["am"] or emergencia["evento"] or emergencia["inicio"]:
                        dados_emergencias.append(emergencia)
                    
                except Exception as e:
                    print(f"      ⚠️ Erro na linha {i}: {e}")
                    continue
            
            print(f"   🎯 TOTAL CAPTURADO: {len(dados_emergencias)} emergências")
            
            if dados_emergencias:
                print("   📋 Primeira emergência capturada:")
                primeira = dados_emergencias[0]
                for chave, valor in primeira.items():
                    if chave not in ["dados_completos", "filtros"]:
                        print(f"      {chave}: {valor}")
            
            return dados_emergencias
            
        except Exception as e:
            print(f"   ❌ Erro na captura: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def salvar_dados(self, dados):
        """Salva dados capturados em arquivo JSON"""
        print("\n💾 Salvando dados...")
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            dados_para_salvar = {
                "emergencias": dados,
                "total_capturado": len(dados),
                "capturado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "fonte": "SPIR Monitor AM",
                "versao": "final_filtros_especificos",
                "filtros_aplicados": {
                    "periodo": "Últimos 15 dias",
                    "estacao_om": "Americana",
                    "estados": ["Aguardando Análise", "Concluído", "Aguardando Execução", "Execução"]
                }
            }
            
            # Arquivo principal
            with open('dados_spir_automatico.json', 'w', encoding='utf-8') as f:
                json.dump(dados_para_salvar, f, ensure_ascii=False, indent=2)
            
            # Backup
            arquivo_backup = f"dados_spir_backup_{timestamp}.json"
            with open(arquivo_backup, 'w', encoding='utf-8') as f:
                json.dump(dados_para_salvar, f, ensure_ascii=False, indent=2)
            
            print(f"   ✅ Dados salvos: dados_spir_automatico.json")
            print(f"   ✅ Backup: {arquivo_backup}")
            print(f"   📊 Total: {len(dados)} emergências")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao salvar: {e}")
            return False
    
    def executar_captura_completa(self):
        """Executa captura completa com filtros específicos"""
        print("🚀 INICIANDO CAPTURA COM FILTROS ESPECÍFICOS")
        print("🎯 Filtros: Americana + Últimos 15 dias + Estados específicos")
        print("=" * 70)
        
        try:
            # Solicitar credenciais
            print("🔐 CREDENCIAIS DO SPIR:")
            usuario = input("👤 Usuário: ").strip()
            
            if not usuario:
                usuario = "8001353"
                print(f"   🔄 Usando usuário padrão: {usuario}")
            
            import getpass
            senha = getpass.getpass("🔑 Senha: ").strip()
            
            # Configurar navegador
            self.configurar_chrome()
            
            # Tentar acesso direto
            if not self.navegar_para_monitor():
                # Fazer login se necessário
                if not self.fazer_login_com_assistencia(usuario, senha):
                    print("❌ Falha no login")
                    return False
                
                # Selecionar empresa
                if not self.selecionar_empresa_paulista_assistido():
                    print("❌ Falha na seleção de empresa")
                    return False
                
                # Navegar para Monitor AM
                if not self.navegar_para_monitor():
                    print("⚠️ Navegue manualmente para Monitor AM")
                    input("👆 PRESSIONE ENTER NO MONITOR AM: ")
            
            # Configurar filtros específicos
            if not self.configurar_filtros_especificos():
                print("❌ Falha na configuração de filtros")
                return False
            
            # Capturar dados
            dados = self.capturar_todas_emergencias()
            
            if not dados:
                print("❌ Nenhum dado capturado")
                return False
            
            # Salvar dados
            if self.salvar_dados(dados):
                print("\n✅ CAPTURA COMPLETA COM SUCESSO!")
                print(f"📊 Total: {len(dados)} emergências")
                print("🎯 Filtros aplicados: Americana + Últimos 15 dias + Estados específicos")
                return True
            else:
                print("❌ Erro ao salvar dados")
                return False
                
        except Exception as e:
            print(f"❌ Erro na execução: {e}")
            return False
        
        finally:
            print("\n⏳ Pressione ENTER para fechar o navegador...")
            input()
            
            if self.driver:
                self.driver.quit()

def main():
    """Função principal"""
    capturador = SPIRAutomaticoFinal()
    
    try:
        sucesso = capturador.executar_captura_completa()
        
        if sucesso:
            print("\n✅ MISSÃO CUMPRIDA COM SUCESSO!")
            print("🎯 Dados filtrados para Americana capturados!")
        else:
            print("\n❌ FALHA NA MISSÃO")
            print("💡 Verifique configurações e filtros")
            
    except KeyboardInterrupt:
        print("\n⏹️ Processo interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    finally:
        if capturador.driver:
            capturador.driver.quit()

if __name__ == "__main__":
    main()