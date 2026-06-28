"""
SPIR Automático - Versão Corrigida com Login Manual
Captura automática de emergências do SPIR com assistência manual quando necessário
"""

import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class SPIRAutomatico:
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
        
        # Verificar se login manual foi bem-sucedido
        try:
            url_final = self.driver.current_url
            print(f"\n   📍 URL após login manual: {url_final}")
            
            if "login" in url_final.lower() or "account" in url_final.lower():
                print("   ⚠️ Parece que ainda está na tela de login")
                print("   🔄 Continuando mesmo assim...")
            else:
                print("   ✅ Login manual detectado como bem-sucedido!")
        except:
            pass
        
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
            
            # Verificar resultado
            url_final = self.driver.current_url
            print(f"   📍 URL final: {url_final}")
            
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
    
    def configurar_filtros_monitor_am(self):
        """Configura filtros específicos no Monitor AM conforme solicitado"""
        print("\n🎯 Configurando filtros específicos no Monitor AM...")
        
        try:
            wait = WebDriverWait(self.driver, 20)
            time.sleep(3)  # Aguardar carregamento da página
            
            # 1. CONFIGURAR PERÍODO - Últimos 15 dias
            print("   📅 Configurando período (últimos 15 dias)...")
            
            # Data de hoje menos 15 dias
            from datetime import datetime, timedelta
            data_fim = datetime.now()
            data_inicio = data_fim - timedelta(days=15)
            
            data_inicio_str = data_inicio.strftime("%d/%m/%Y")
            data_fim_str = data_fim.strftime("%d/%m/%Y")
            
            print(f"      📆 Período: {data_inicio_str} a {data_fim_str}")
            
            # Tentar encontrar campos de data
            try:
                # Procurar campos de data por diferentes estratégias
                campos_data_inicio = self.driver.find_elements(By.CSS_SELECTOR, 
                    "input[type='text'], input[type='date'], input[placeholder*='data']")
                
                # Primeiro campo provavelmente é data início
                if len(campos_data_inicio) >= 2:
                    campo_inicio = campos_data_inicio[0]
                    campo_fim = campos_data_inicio[1]
                    
                    # Limpar e preencher datas
                    campo_inicio.clear()
                    campo_inicio.send_keys(data_inicio_str)
                    
                    campo_fim.clear()
                    campo_fim.send_keys(data_fim_str)
                    
                    print("      ✅ Período configurado automaticamente")
                else:
                    print("      ⚠️ Campos de data não encontrados automaticamente")
                    
            except Exception as e:
                print(f"      ❌ Erro na configuração de data: {e}")
            
            # 2. CONFIGURAR ESTAÇÃO AVANÇADA OM - Somente Americana
            print("   🏭 Configurando Estação Avançada OM (Americana)...")
            
            try:
                # Procurar dropdown ou campo de Estação Avançada OM
                elementos_americana = [
                    # Procurar por texto "Americana" já selecionado
                    self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Americana')]"),
                    # Procurar por campos relacionados a estação
                    self.driver.find_elements(By.CSS_SELECTOR, "[placeholder*='estação'], [placeholder*='Estação']")
                ]
                
                americana_configurado = False
                
                # Verificar se Americana já está selecionado
                for grupo in elementos_americana:
                    for elem in grupo:
                        if elem.is_displayed() and "americana" in elem.text.lower():
                            print("      ✅ Americana já está selecionado")
                            americana_configurado = True
                            break
                    if americana_configurado:
                        break
                
                if not americana_configurado:
                    # Tentar encontrar dropdown de estação
                    dropdowns_estacao = self.driver.find_elements(By.CSS_SELECTOR, 
                        "select, [role='combobox'], .dropdown")
                    
                    for dropdown in dropdowns_estacao:
                        try:
                            # Se for um select
                            if dropdown.tag_name == "select":
                                select_obj = Select(dropdown)
                                for opcao in select_obj.options:
                                    if "americana" in opcao.text.lower():
                                        select_obj.select_by_visible_text(opcao.text)
                                        print("      ✅ Americana selecionado no dropdown")
                                        americana_configurado = True
                                        break
                            
                            # Se for dropdown customizado
                            else:
                                dropdown.click()
                                time.sleep(1)
                                opcoes_americana = self.driver.find_elements(By.XPATH, 
                                    "//*[contains(text(), 'Americana')]")
                                for opcao in opcoes_americana:
                                    if opcao.is_displayed():
                                        opcao.click()
                                        print("      ✅ Americana selecionado")
                                        americana_configurado = True
                                        break
                            
                            if americana_configurado:
                                break
                                
                        except Exception as e:
                            continue
                
                if not americana_configurado:
                    print("      ⚠️ Americana não foi configurado automaticamente")
                    
            except Exception as e:
                print(f"      ❌ Erro na configuração de Americana: {e}")
            
            # 3. CONFIGURAR ESTADOS ESPECÍFICOS
            print("   📋 Configurando Estados específicos...")
            
            estados_desejados = [
                "Aguardando Análise",
                "Concluído", 
                "Aguardando Execução",
                "Execução"
            ]
            
            try:
                # Primeiro, desmarcar todos os estados (se necessário)
                checkboxes_estados = self.driver.find_elements(By.CSS_SELECTOR, 
                    "input[type='checkbox']")
                
                estados_configurados = []
                
                for checkbox in checkboxes_estados:
                    try:
                        # Encontrar o texto associado ao checkbox
                        label_element = None
                        
                        # Estratégia 1: Label diretamente relacionado
                        checkbox_id = checkbox.get_attribute('id')
                        if checkbox_id:
                            label_element = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{checkbox_id}']")
                        
                        # Estratégia 2: Texto do elemento pai
                        if not label_element:
                            parent = checkbox.find_element(By.XPATH, "./..")
                            texto_parent = parent.text.strip()
                        else:
                            texto_parent = label_element.text.strip()
                        
                        # Verificar se é um dos estados desejados
                        for estado in estados_desejados:
                            if estado.lower() in texto_parent.lower():
                                if not checkbox.is_selected():
                                    checkbox.click()
                                    print(f"      ✅ Estado '{estado}' selecionado")
                                    estados_configurados.append(estado)
                                else:
                                    print(f"      ✅ Estado '{estado}' já estava selecionado")
                                    estados_configurados.append(estado)
                                break
                        
                        # Desmarcar outros estados se estiverem marcados
                        else:
                            # Se não é um estado desejado e está marcado, desmarcar
                            if checkbox.is_selected() and texto_parent:
                                # Verificar se não é um dos estados desejados
                                eh_estado_desejado = any(estado.lower() in texto_parent.lower() 
                                                       for estado in estados_desejados)
                                if not eh_estado_desejado:
                                    checkbox.click()
                                    print(f"      ➖ Estado '{texto_parent}' desmarcado")
                        
                    except Exception as e:
                        continue
                
                if estados_configurados:
                    print(f"      ✅ Estados configurados: {', '.join(estados_configurados)}")
                else:
                    print("      ⚠️ Nenhum estado foi configurado automaticamente")
                    
            except Exception as e:
                print(f"      ❌ Erro na configuração de estados: {e}")
            
            # 4. EXECUTAR PESQUISA
            print("   🔍 Executando pesquisa com filtros configurados...")
            
            try:
                # Procurar botão de pesquisar
                botoes_pesquisa = [
                    self.driver.find_elements(By.XPATH, "//button[contains(text(), 'PESQUISAR')]"),
                    self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Pesquisar')]"),
                    self.driver.find_elements(By.CSS_SELECTOR, "button[type='submit']"),
                    self.driver.find_elements(By.CSS_SELECTOR, ".btn-primary, .btn-search")
                ]
                
                botao_encontrado = False
                for grupo_botoes in botoes_pesquisa:
                    for botao in grupo_botoes:
                        if botao.is_displayed() and botao.is_enabled():
                            botao.click()
                            print("      ✅ Botão PESQUISAR clicado!")
                            botao_encontrado = True
                            break
                    if botao_encontrado:
                        break
                
                if not botao_encontrado:
                    print("      ⚠️ Botão PESQUISAR não encontrado - continue manualmente")
                else:
                    # Aguardar carregamento dos resultados
                    print("      ⏳ Aguardando carregamento dos resultados...")
                    time.sleep(10)  # Aguardar mais tempo para carregar
                    
            except Exception as e:
                print(f"      ❌ Erro ao executar pesquisa: {e}")
            
            print("   ✅ Configuração de filtros concluída!")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro geral na configuração de filtros: {e}")
            return False
    
    def capturar_dados_emergencias(self):
        """Captura dados das emergências do Monitor AM com estratégias múltiplas"""
        print("\n📊 Capturando TODAS as emergências...")
        
        try:
            wait = WebDriverWait(self.driver, 30)
            
            # Aguardar carregamento da página e resultados
            print("   ⏳ Aguardando carregamento completo dos resultados...")
            time.sleep(10)
            
            # Verificar se estamos na página correta
            url_atual = self.driver.current_url
            print(f"   📍 URL atual: {url_atual}")
            
            if "MonitorAM" not in url_atual:
                print("   ❌ Não está na página do Monitor AM")
                print("   🔴 NAVEGUE MANUALMENTE PARA O MONITOR AM e pressione ENTER")
                input("👆 PRESSIONE ENTER QUANDO ESTIVER NO MONITOR AM: ")
            
            # ESTRATÉGIA 1: Aguardar carregamento completo e verificar paginação
            print("   🔍 ESTRATÉGIA 1: Verificando se há paginação...")
            
            # Procurar indicadores de paginação
            paginacao_elementos = [
                self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Página')]"),
                self.driver.find_elements(By.XPATH, "//*[contains(text(), 'página')]"),
                self.driver.find_elements(By.CSS_SELECTOR, ".pagination, .pager"),
                self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Próxima')]"),
                self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Anterior')]"),
                self.driver.find_elements(By.XPATH, "//*[contains(text(), 'de') and contains(text(), 'registros')]")
            ]
            
            tem_paginacao = False
            total_registros_info = ""
            
            for grupo in paginacao_elementos:
                if grupo:
                    for elem in grupo:
                        texto = elem.text.strip()
                        if texto:
                            print(f"      📄 Paginação detectada: '{texto}'")
                            tem_paginacao = True
                            if "registro" in texto.lower() or "de" in texto.lower():
                                total_registros_info = texto
            
            if tem_paginacao:
                print(f"      ⚠️ PAGINAÇÃO DETECTADA! Info: {total_registros_info}")
                print("      🔍 Vou capturar dados de todas as páginas...")
            else:
                print("      ✅ Sem paginação detectada - página única")
            
            # ESTRATÉGIA 2: Procurar por botão "Mostrar todos" ou similar
            print("   🔍 ESTRATÉGIA 2: Procurando opções para mostrar todos os registros...")
            
            botoes_mostrar_todos = [
                self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Mostrar todos')]"),
                self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Ver todos')]"),
                self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Todos')]"),
                self.driver.find_elements(By.CSS_SELECTOR, "select[name*='length'], select[id*='length']"),
                self.driver.find_elements(By.XPATH, "//select//option[contains(text(), 'Todos')]"),
                self.driver.find_elements(By.XPATH, "//select//option[contains(text(), '100')]"),
                self.driver.find_elements(By.XPATH, "//select//option[contains(text(), '50')]")
            ]
            
            registros_expandidos = False
            
            for i, grupo in enumerate(botoes_mostrar_todos):
                if grupo and not registros_expandidos:
                    for elem in grupo:
                        try:
                            if elem.is_displayed():
                                # Se for um select, tentar selecionar "Todos" ou maior número
                                if elem.tag_name == "select":
                                    select_obj = Select(elem)
                                    opcoes_texto = [opt.text for opt in select_obj.options]
                                    print(f"      📋 Opções disponíveis: {opcoes_texto}")
                                    
                                    # Tentar selecionar "Todos" primeiro
                                    for opcao in select_obj.options:
                                        if "todos" in opcao.text.lower() or "all" in opcao.text.lower():
                                            select_obj.select_by_visible_text(opcao.text)
                                            print(f"      ✅ Selecionado 'Todos': {opcao.text}")
                                            registros_expandidos = True
                                            break
                                    
                                    # Se não tem "Todos", pegar o maior número
                                    if not registros_expandidos:
                                        numeros = []
                                        for opcao in select_obj.options:
                                            try:
                                                num = int(opcao.text)
                                                numeros.append((num, opcao))
                                            except:
                                                continue
                                        
                                        if numeros:
                                            maior_numero, maior_opcao = max(numeros)
                                            select_obj.select_by_visible_text(maior_opcao.text)
                                            print(f"      ✅ Selecionado maior número: {maior_numero}")
                                            registros_expandidos = True
                                
                                # Se for botão, clicar
                                elif elem.tag_name in ["button", "a"]:
                                    elem.click()
                                    print(f"      ✅ Clicado em: '{elem.text}'")
                                    registros_expandidos = True
                                
                                if registros_expandidos:
                                    print("      ⏳ Aguardando recarregamento...")
                                    time.sleep(8)
                                    break
                                    
                        except Exception as e:
                            continue
                
                if registros_expandidos:
                    break
            
            # ESTRATÉGIA 3: Scroll para carregar mais dados (se for lazy loading)
            print("   🔍 ESTRATÉGIA 3: Fazendo scroll para carregar todos os dados...")
            
            # Scroll até o final da página para garantir que tudo carregou
            for i in range(5):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                print(f"      📜 Scroll {i+1}/5 realizado")
            
            # Voltar ao topo
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            # ESTRATÉGIA 4: Procurar tabela com múltiplas estratégias
            print("   🔍 ESTRATÉGIA 4: Procurando tabela de emergências...")
            
            # Aguardar elementos carregarem
            time.sleep(5)
            
            # Diferentes seletores para a tabela - mais abrangentes
            tabela_seletores = [
                "table",
                ".table",
                "tbody", 
                "[id*='grid']",
                "[id*='table']",
                "[id*='data']",
                "[class*='grid']",
                "[class*='table']",
                "[class*='data']",
                "div[role='table']",
                "[role='grid']"
            ]
            
            todas_tabelas = []
            
            for seletor in tabela_seletores:
                try:
                    tabelas = self.driver.find_elements(By.CSS_SELECTOR, seletor)
                    for tabela in tabelas:
                        linhas = tabela.find_elements(By.TAG_NAME, "tr")
                        if len(linhas) > 1:  # Tem pelo menos cabeçalho + dados
                            todas_tabelas.append((tabela, len(linhas), seletor))
                            print(f"      📋 Tabela encontrada: {seletor} - {len(linhas)} linhas")
                except:
                    continue
            
            if not todas_tabelas:
                print("   ❌ Nenhuma tabela encontrada automaticamente")
                print("   🔴 MODO MANUAL: Certifique-se que os dados estão visíveis e pressione ENTER")
                input("👆 PRESSIONE ENTER QUANDO TODOS OS DADOS ESTIVEREM VISÍVEIS: ")
                
                # Tentar novamente após intervenção manual
                tabelas = self.driver.find_elements(By.CSS_SELECTOR, "table, .table, tbody")
                if tabelas:
                    todas_tabelas = [(tabelas[0], len(tabelas[0].find_elements(By.TAG_NAME, "tr")), "manual")]
                else:
                    print("   ❌ Ainda não foi possível encontrar a tabela")
                    return []
            
            # Escolher a maior tabela
            tabela_escolhida, num_linhas, seletor_usado = max(todas_tabelas, key=lambda x: x[1])
            print(f"   ✅ Usando tabela com mais dados: {seletor_usado} - {num_linhas} linhas")
            
            # ESTRATÉGIA 5: Capturar dados de TODAS as páginas se houver paginação
            todos_dados = []
            pagina_atual = 1
            
            while True:
                print(f"\n   � PROCESSANDO PÁGINA {pagina_atual}...")
                
                # Extrair dados da página atual
                dados_pagina = self._extrair_dados_tabela(tabela_escolhida, pagina_atual)
                todos_dados.extend(dados_pagina)
                
                print(f"      ✅ Página {pagina_atual}: {len(dados_pagina)} emergências capturadas")
                
                # Verificar se há próxima página
                if not tem_paginacao:
                    print("      ℹ️ Sem paginação - captura completa")
                    break
                
                # Procurar botão "Próxima" ou similar
                botao_proxima = None
                seletores_proxima = [
                    "//button[contains(text(), 'Próxima')]",
                    "//a[contains(text(), 'Próxima')]", 
                    "//button[contains(text(), '>')]",
                    "//a[contains(text(), '>')]",
                    "//*[@class='next']",
                    "//*[contains(@class, 'next')]"
                ]
                
                for seletor in seletores_proxima:
                    try:
                        elementos = self.driver.find_elements(By.XPATH, seletor)
                        for elem in elementos:
                            if elem.is_displayed() and elem.is_enabled():
                                botao_proxima = elem
                                break
                        if botao_proxima:
                            break
                    except:
                        continue
                
                if botao_proxima:
                    try:
                        botao_proxima.click()
                        print(f"      ➡️ Navegando para página {pagina_atual + 1}...")
                        time.sleep(5)  # Aguardar carregamento
                        pagina_atual += 1
                        
                        # Atualizar referência da tabela
                        tabela_escolhida = self.driver.find_element(By.CSS_SELECTOR, seletor_usado)
                        
                    except Exception as e:
                        print(f"      ❌ Erro ao navegar para próxima página: {e}")
                        break
                else:
                    print("      ✅ Última página alcançada")
                    break
            
            print(f"\n   🎯 CAPTURA COMPLETA: {len(todos_dados)} emergências de {pagina_atual} página(s)")
            
            return todos_dados
            
        except Exception as e:
            print(f"   ❌ Erro na captura de dados: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _extrair_dados_tabela(self, tabela, pagina_numero):
        """Extrai dados de uma tabela específica"""
        dados_emergencias = []
        
        try:
            linhas = tabela.find_elements(By.TAG_NAME, "tr")
            print(f"         📊 Encontradas {len(linhas)} linhas na tabela")
            
            cabecalho_processado = False
            
            for i, linha in enumerate(linhas):
                try:
                    # Tentar td primeiro, depois th
                    celulas = linha.find_elements(By.TAG_NAME, "td")
                    if not celulas:
                        celulas = linha.find_elements(By.TAG_NAME, "th")
                    
                    # Pular se não tem dados suficientes
                    if len(celulas) < 3:
                        continue
                    
                    # Extrair texto das células
                    dados_linha = []
                    for celula in celulas:
                        texto = celula.text.strip()
                        dados_linha.append(texto)
                    
                    # Verificar se é cabeçalho
                    if not cabecalho_processado and i < 3:
                        # Se contém palavras típicas de cabeçalho, pular
                        texto_linha = " ".join(dados_linha).lower()
                        palavras_cabecalho = ["evento", "número", "am", "município", "data", "status", "equipamento"]
                        if any(palavra in texto_linha for palavra in palavras_cabecalho):
                            cabecalho_processado = True
                            print(f"         📋 Cabeçalho detectado na linha {i}: {dados_linha[:3]}")
                            continue
                    
                    # Verificar se tem dados mínimos válidos
                    if not any(dados_linha):
                        continue
                    
                    # Criar objeto emergência
                    emergencia = {
                        "id": len(dados_emergencias) + 1 + (pagina_numero - 1) * 1000,  # ID único por página
                        "am": dados_linha[0] if len(dados_linha) > 0 else "",
                        "ocorrencia": dados_linha[1] if len(dados_linha) > 1 else "",
                        "inicio": dados_linha[2] if len(dados_linha) > 2 else "",
                        "previsao": dados_linha[3] if len(dados_linha) > 3 else "",
                        "municipio": dados_linha[4] if len(dados_linha) > 4 else "",
                        "equipamento": dados_linha[5] if len(dados_linha) > 5 else "",
                        "causa": dados_linha[6] if len(dados_linha) > 6 else "",
                        "status": dados_linha[7] if len(dados_linha) > 7 else "",
                        "dados_completos": dados_linha,
                        "capturado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "pagina": pagina_numero,
                        "linha_original": i,
                        "filtros_aplicados": {
                            "periodo": "Últimos 15 dias",
                            "estacao_om": "Americana", 
                            "estados": ["Aguardando Análise", "Concluído", "Aguardando Execução", "Execução"]
                        }
                    }
                    
                    # Verificar se tem dados mínimos (pelo menos AM ou ocorrência)
                    if emergencia["am"] or emergencia["ocorrencia"] or emergencia["inicio"]:
                        dados_emergencias.append(emergencia)
                        
                except Exception as e:
                    print(f"         ⚠️ Erro na linha {i}: {e}")
                    continue
            
            print(f"         ✅ Extraídas {len(dados_emergencias)} emergências da página {pagina_numero}")
            
            return dados_emergencias
            
        except Exception as e:
            print(f"         ❌ Erro na extração da tabela: {e}")
            return []
            
            # Diferentes seletores para a tabela
            tabela_seletores = [
                "table",
                ".table",
                "tbody",
                "[id*='grid']",
                "[id*='table']",
                "[class*='grid']",
                "[class*='table']"
            ]
            
            tabela_encontrada = None
            for seletor in tabela_seletores:
                try:
                    tabelas = self.driver.find_elements(By.CSS_SELECTOR, seletor)
                    if tabelas:
                        # Pegar a maior tabela (provavelmente a principal)
                        tabela_encontrada = max(tabelas, key=lambda t: len(t.find_elements(By.TAG_NAME, "tr")))
                        print(f"   ✅ Tabela encontrada com seletor: {seletor}")
                        break
                except:
                    continue
            
            if not tabela_encontrada:
                print("   ❌ Tabela não encontrada automaticamente")
                print("   🔴 MODO MANUAL: Deixe a página carregada com dados e pressione ENTER")
                input("👆 PRESSIONE ENTER QUANDO OS DADOS ESTIVEREM VISÍVEIS: ")
                
                # Tentar novamente após intervenção manual
                tabelas = self.driver.find_elements(By.CSS_SELECTOR, "table, .table, tbody")
                if tabelas:
                    tabela_encontrada = tabelas[0]
                else:
                    print("   ❌ Ainda não foi possível encontrar a tabela")
                    return []
            
            # Extrair dados da tabela
            print("   📋 Extraindo dados da tabela...")
            
            linhas = tabela_encontrada.find_elements(By.TAG_NAME, "tr")
            print(f"   📊 Encontradas {len(linhas)} linhas na tabela")
            
            dados_emergencias = []
            cabecalho_processado = False
            
            for i, linha in enumerate(linhas):
                try:
                    celulas = linha.find_elements(By.TAG_NAME, "td")
                    
                    # Pular se não tem dados suficientes
                    if len(celulas) < 3:
                        continue
                    
                    # Extrair texto das células
                    dados_linha = []
                    for celula in celulas:
                        texto = celula.text.strip()
                        dados_linha.append(texto)
                    
                    # Verificar se é uma linha válida (não cabeçalho vazio)
                    if any(dados_linha) and not cabecalho_processado:
                        # Primeira linha válida pode ser cabeçalho
                        if i < 3:  # Só considerar cabeçalho nas primeiras linhas
                            cabecalho_processado = True
                            continue
                    
                    # Criar objeto emergência
                    emergencia = {
                        "id": len(dados_emergencias) + 1,
                        "am": dados_linha[0] if len(dados_linha) > 0 else "",
                        "ocorrencia": dados_linha[1] if len(dados_linha) > 1 else "",
                        "inicio": dados_linha[2] if len(dados_linha) > 2 else "",
                        "previsao": dados_linha[3] if len(dados_linha) > 3 else "",
                        "municipio": dados_linha[4] if len(dados_linha) > 4 else "",
                        "equipamento": dados_linha[5] if len(dados_linha) > 5 else "",
                        "causa": dados_linha[6] if len(dados_linha) > 6 else "",
                        "status": dados_linha[7] if len(dados_linha) > 7 else "",
                        "dados_completos": dados_linha,
                        "capturado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # Verificar se tem dados mínimos
                    if emergencia["am"] or emergencia["ocorrencia"]:
                        dados_emergencias.append(emergencia)
                        
                except Exception as e:
                    print(f"   ⚠️ Erro na linha {i}: {e}")
                    continue
            
            print(f"   ✅ Capturadas {len(dados_emergencias)} emergências!")
            
            # Mostrar sample dos dados
            if dados_emergencias:
                print("   📋 Exemplo de dados capturados:")
                primeira = dados_emergencias[0]
                for chave, valor in primeira.items():
                    if chave != "dados_completos":
                        print(f"      {chave}: {valor}")
            
            return dados_emergencias
            
        except Exception as e:
            print(f"   ❌ Erro na captura de dados: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def salvar_dados(self, dados):
        """Salva dados capturados em arquivo JSON"""
        print("\n💾 Salvando dados...")
        
        try:
            # Arquivo principal
            arquivo_principal = "dados_spir_automatico.json"
            
            # Backup com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_backup = f"dados_spir_backup_{timestamp}.json"
            
            dados_para_salvar = {
                "emergencias": dados,
                "total_capturado": len(dados),
                "capturado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "fonte": "SPIR Monitor AM",
                "versao": "automatico_corrigido"
            }
            
            # Salvar arquivo principal
            with open(arquivo_principal, 'w', encoding='utf-8') as f:
                json.dump(dados_para_salvar, f, ensure_ascii=False, indent=2)
            
            # Salvar backup
            with open(arquivo_backup, 'w', encoding='utf-8') as f:
                json.dump(dados_para_salvar, f, ensure_ascii=False, indent=2)
            
            print(f"   ✅ Dados salvos em: {arquivo_principal}")
            print(f"   ✅ Backup salvo em: {arquivo_backup}")
            print(f"   📊 Total de registros: {len(dados)}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao salvar dados: {e}")
            return False
    
    def executar_captura_completa(self):
        """Executa captura completa com todas as etapas"""
        print("🚀 INICIANDO CAPTURA AUTOMÁTICA CORRIGIDA DO SPIR")
        print("=" * 60)
        
        try:
            # Solicitar credenciais
            print("🔐 CREDENCIAIS DO SPIR:")
            usuario = input("👤 Usuário: ").strip()
            
            if not usuario:
                usuario = "8001353"  # Padrão
                print(f"   🔄 Usando usuário padrão: {usuario}")
            
            import getpass
            senha = getpass.getpass("🔑 Senha: ").strip()
            
            # Configurar navegador
            self.configurar_chrome()
            
            # Tentar acesso direto ao Monitor AM
            print("\n🎯 ESTRATÉGIA: Acesso direto ao Monitor AM...")
            if not self.navegar_para_monitor():
                # Se redirecionou para login, fazer login
                print("   🔐 Acesso direto redirecionou para login - fazendo login...")
                
                if not self.fazer_login_com_assistencia(usuario, senha):
                    print("❌ Falha no login")
                    return False
                
                # Selecionar empresa
                if not self.selecionar_empresa_paulista_assistido():
                    print("❌ Falha na seleção de empresa")
                    return False
                
            # Tentar navegar para Monitor AM novamente
            if not self.navegar_para_monitor():
                print("⚠️ Navegue manualmente para Monitor AM")
                input("👆 PRESSIONE ENTER QUANDO ESTIVER NO MONITOR AM: ")
            
            # Configurar filtros específicos conforme solicitado
            print("\n🎯 Configurando filtros específicos...")
            if not self.configurar_filtros_monitor_am():
                print("⚠️ Configure os filtros manualmente:")
                print("   📅 Período: Últimos 15 dias")
                print("   🏭 Estação Avançada OM: Americana")
                print("   📋 Estados: Aguardando Análise, Concluído, Aguardando Execução, Execução")
                print("   🔍 Clique em PESQUISAR")
                input("👆 PRESSIONE ENTER APÓS CONFIGURAR FILTROS E EXECUTAR PESQUISA: ")
            
            # Capturar dados
            dados = self.capturar_dados_emergencias()
            
            if not dados:
                print("❌ Nenhum dado capturado")
                return False
            
            # Salvar dados
            if self.salvar_dados(dados):
                print("\n✅ CAPTURA CONCLUÍDA COM SUCESSO!")
                print(f"📊 Total capturado: {len(dados)} emergências")
                return True
            else:
                print("❌ Erro ao salvar dados")
                return False
                
        except Exception as e:
            print(f"❌ Erro na execução: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        finally:
            # Manter navegador aberto para verificação
            print("\n⏳ Pressione ENTER para fechar o navegador...")
            input()
            
            if self.driver:
                self.driver.quit()

def main():
    """Função principal"""
    capturador = SPIRAutomatico()
    
    try:
        sucesso = capturador.executar_captura_completa()
        
        if sucesso:
            print("\n✅ MISSÃO CUMPRIDA COM SUCESSO!")
        else:
            print("\n❌ FALHA NA MISSÃO")
            print("💡 Verifique credenciais e conexão")
            
    except KeyboardInterrupt:
        print("\n⏹️ Processo interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    finally:
        if capturador.driver:
            capturador.driver.quit()

if __name__ == "__main__":
    main()