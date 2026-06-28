#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 SPIR AUTOMÁTICO TOTAL - Login + Captura Completa
Script 100% automatizado para buscar emergências no SPIR
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from datetime import datetime
import getpass

class SPIRAutomatico:
    def __init__(self):
        self.driver = None
        self.emergencias = []
        
    def configurar_chrome(self):
        """Configura o Chrome com opções otimizadas"""
        print("🔧 Configurando Chrome...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Executar script para evitar detecção
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Chrome configurado com sucesso!")
        
    def fazer_login(self, usuario, senha):
        """Faz login automático no SPIR"""
        print("🔐 Fazendo login no SPIR...")
        
        try:
            # Acessar página de login
            self.driver.get("https://spir.cpfl.com.br/")
            
            # Aguardar carregamento com mais tempo
            wait = WebDriverWait(self.driver, 30)
            time.sleep(3)  # Aguardar carregamento inicial
            
            # Encontrar campos de login
            print("   🔍 Procurando campos de login...")
            
            usuario_seletores = [
                "input[name='username']",
                "input[name='user']", 
                "input[name='login']",
                "input[type='text']",
                "input[id*='user']",
                "input[placeholder*='usuário']",
                "input[placeholder*='user']"
            ]
            
            senha_seletores = [
                "input[name='password']",
                "input[name='senha']",
                "input[type='password']",
                "input[id*='pass']",
                "input[placeholder*='senha']",
                "input[placeholder*='password']"
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
            
            if not campo_usuario:
                print("❌ Campo usuário não encontrado!")
                return False
            
            # Encontrar campo senha
            campo_senha = None
            for seletor in senha_seletores:
                try:
                    campo_senha = self.driver.find_element(By.CSS_SELECTOR, seletor)
                    print(f"   ✅ Campo senha encontrado: {seletor}")
                    break
                except:
                    continue
                    
            if not campo_senha:
                print("❌ Campo senha não encontrado!")
                return False
            
            # Preencher credenciais
            print("   📝 Preenchendo credenciais...")
            wait.until(EC.element_to_be_clickable(campo_usuario))
            
            campo_usuario.click()
            campo_usuario.clear()
            time.sleep(0.5)
            campo_usuario.send_keys(usuario)
            
            wait.until(EC.element_to_be_clickable(campo_senha))
            campo_senha.click()
            campo_senha.clear()
            time.sleep(0.5)
            campo_senha.send_keys(senha)
            
            botao_seletores = [
                "button[type='submit']",
                "input[type='submit']",
                "button[class*='login']",
                "button[class*='entrar']",
                ".btn-login",
                ".login-button"
            ]
            
            botao_login = None
            for seletor in botao_seletores:
                try:
                    botao_login = self.driver.find_element(By.CSS_SELECTOR, seletor)
                    print(f"   ✅ Botão login encontrado: {seletor}")
                    break
                except:
                    continue
            
            if botao_login:
                botao_login.click()
            else:
                campo_senha.send_keys(Keys.RETURN)
            
            print("   ⏳ Aguardando login processar (até 15 segundos)...")
            time.sleep(10)
            
            try:
                WebDriverWait(self.driver, 15).until(
                    lambda driver: "login" not in driver.current_url.lower() or 
                            "GestaoAcessosMultiempresa" not in driver.current_url
                )
                print("✅ Página mudou após login!")
            except:
                print("⏳ Timeout aguardando mudança de URL...")
                pass
            
            url_atual = self.driver.current_url
            print(f"   📍 URL após tentativa de login: {url_atual[:80]}...")
            
            try:
                login_form = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                if login_form.is_displayed():
                    print("❌ Ainda na página de login - credenciais inválidas!")
                    return False
            except:
                pass
            
            if "login" not in url_atual.lower() or "GestaoAcessosMultiempresa" not in url_atual:
                print("✅ Login realizado com sucesso!")
                time.sleep(3)
                
                if self.selecionar_empresa_paulista():
                    return True
                else:
                    print("⚠️ Login OK, mas erro na seleção de empresa")
                    return False
            else:
                print("❌ Falha no login - verifique credenciais")
                return False
                
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            return False
    
    def selecionar_empresa_paulista(self):
        """Seleciona empresa Paulista após login"""
        print("🏢 Selecionando empresa Paulista...")
        
        try:
            wait = WebDriverWait(self.driver, 25)
            time.sleep(3)
            
            print("   🔍 PASSO 1: Procurando 'Paulista' na página...")
            paulista_clicado = False
            
            seletores_paulista = [
                "//*[contains(text(), 'Paulista')]",
                "//div[contains(., 'Paulista')]",
                "//button[contains(text(), 'Paulista')]",
                "//a[contains(text(), 'Paulista')]",
            ]
            
            for seletor in seletores_paulista:
                try:
                    elementos = self.driver.find_elements(By.XPATH, seletor)
                    for elem in elementos:
                        if elem.is_displayed():
                            texto = elem.text.strip()
                            if texto and "Empresas" not in texto and len(texto) < 50:
                                self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                                time.sleep(0.5)
                                elem.click()
                                paulista_clicado = True
                                time.sleep(2)
                                break
                    if paulista_clicado:
                        break
                except:
                    continue
            
            if not paulista_clicado:
                print("      ⚠️ Não encontrou Paulista para clicar - pode já estar selecionado!")
            
            print("   🔍 PASSO 2: Procurando e clicando no botão OK...")
            botao_ok = None
            seletores_ok = [
                "//button[text()='OK']",
                "//button[contains(text(), 'OK')]",
                "//input[@value='OK'][@type='submit']",
                "//*[@type='submit'][contains(text(), 'OK')]"
            ]
            
            for seletor in seletores_ok:
                try:
                    elementos_ok = self.driver.find_elements(By.XPATH, seletor)
                    for elem in elementos_ok:
                        if elem.is_displayed() and elem.is_enabled():
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                            time.sleep(0.5)
                            elem.click()
                            botao_ok = elem
                            time.sleep(3)
                            break
                    if botao_ok:
                        break
                except:
                    continue
            
            if not botao_ok:
                try:
                    self.driver.execute_script("""
                        var buttons = document.querySelectorAll('button');
                        for(var btn of buttons) {
                            if(btn.innerText.trim() === 'OK' && btn.offsetParent !== null) {
                                btn.click();
                                break;
                            }
                        }
                    """)
                    time.sleep(3)
                except Exception as e:
                    print(f"      ❌ Falha no clique JavaScript: {e}")
                    return False
            
            print("   ⏳ Aguardando redirecionamento após clique em OK...")
            time.sleep(5)
            return True
            
        except Exception as e:
            print(f"❌ Erro na seleção de empresa: {e}")
            return False
    
    def navegar_para_monitor(self):
        """Navega DIRETAMENTE para o Monitor AM"""
        print("🗺️ Navegando DIRETAMENTE para Monitor AM...")
        
        try:
            url_monitor = "https://spir.cpfl.com.br/Consultas/MonitorAM/Visualizar"
            self.driver.get(url_monitor)
            time.sleep(5)
            
            url_atual = self.driver.current_url
            if "MonitorAM" in url_atual or "Visualizar" in url_atual:
                print("✅ Monitor AM acessado diretamente com sucesso!")
                return True
            else:
                return True
                
        except Exception as e:
            print(f"❌ Erro na navegação: {e}")
            return False
    
    def configurar_filtros_automatico(self):
        """Configura filtros automaticamente para mostrar todas as emergências"""
        print("⚙️ Configurando filtros automaticamente...")
        
        try:
            time.sleep(5)
            
            print("   🔍 Configurando estação...")
            try:
                estacao_elem = None
                for seletor in ["EstacaoId", "[id*='Estacao']", "select[name*='Estacao']"]:
                    try:
                        estacao_elem = self.driver.find_element(By.CSS_SELECTOR, seletor)
                        break
                    except:
                        continue
                
                if estacao_elem:
                    estacao_select = Select(estacao_elem)
                    for option in estacao_select.options:
                        if "Americana" in option.text:
                            estacao_select.select_by_visible_text(option.text)
                            print("      ... Estação OM Americana selecionada")
                            break
            except Exception as e:
                print(f"      ⚠️ Erro na estação: {e}")
            
            print("   📅 Configurando período...")
            try:
                periodo_elem = None
                for seletor in ["PeriodoId", "[id*='Periodo']", "select[name*='Periodo']"]:
                    try:
                        periodo_elem = self.driver.find_element(By.CSS_SELECTOR, seletor)
                        break
                    except:
                        continue
                        
                if periodo_elem:
                    periodo_select = Select(periodo_elem)
                    for option in periodo_select.options:
                        if "15" in option.text or "30" in option.text:
                            periodo_select.select_by_visible_text(option.text)
                            print("      ... Período configurado com sucesso")
                            break
            except Exception as e:
                print(f"      ⚠️ Erro no período: {e}")
            
            print("   📊 Configurando status...")
            try:
                icheck_helpers = self.driver.find_elements(By.CLASS_NAME, "iCheck-helper")
                if icheck_helpers:
                    for helper in icheck_helpers:
                        try:
                            self.driver.execute_script("arguments[0].click();", helper)
                        except:
                            continue
                    print("      ✅ Todos os status marcados via máscara iCheck!")
                else:
                    self.driver.execute_script("""
                        var checkboxes = document.querySelectorAll("input[type='checkbox']");
                        checkboxes.forEach(function(cb) {
                            if(!cb.checked) { cb.click(); }
                        });
                    """)
            except Exception as e:
                print(f"      ⚠️ Erro ao marcar status: {e}")
            
            time.sleep(2)
            
            print("   🔍 Executando pesquisa...")
            botoes_pesquisa = [
                "button[type='submit']",
                "input[type='submit']", 
                "button[class*='pesquisar']",
                "button[class*='filtrar']",
                ".btn-primary",
                ".btn-search"
            ]
            
            for seletor in botoes_pesquisa:
                try:
                    botao = self.driver.find_element(By.CSS_SELECTOR, seletor)
                    botao.click()
                    break
                except:
                    continue
            
            print("   ⏳ Aguardando resultados...")
            time.sleep(10)
            return True
            
        except Exception as e:
            print(f"❌ Erro na configuração de filtros: {e}")
            return False
    
    def capturar_emergencias_total(self):
        """Captura todas as emergências da página"""
        print("📊 Capturando todas as emergências...")
        
        try:
            time.sleep(5)
            
            print("   📜 Fazendo scroll para carregar dados...")
            for i in range(5):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            tabelas = self.driver.find_elements(By.TAG_NAME, "table")
            emergencias_encontradas = []
            
            for i, tabela in enumerate(tabelas):
                try:
                    linhas = tabela.find_elements(By.TAG_NAME, "tr")
                    for j, linha in enumerate(linhas[1:], 1):
                        try:
                            cells = linha.find_elements(By.TAG_NAME, "td")
                            if len(cells) >= 3:
                                dados = [cell.text.strip() for cell in cells]
                                if any(dados):
                                    # ESTRUTURA SINCRONIZADA CORRETAMENTE COM O DASHBOARD HTML
                                    emergencia = {
                                        "evento": dados[2] if len(dados) > 2 else (dados[0] if len(dados) > 0 else ""),
                                        "am": dados[3] if len(dados) > 3 else (dados[1] if len(dados) > 1 else ""),
                                        "municipio": dados[4] if len(dados) > 4 else "Americana",
                                        "data_criacao": datetime.now().strftime("%d/%m/%Y"),
                                        "materiais": "Materiais diversos de rede",
                                        "status": dados[1] if len(dados) > 1 else "Aguardando Execução",
                                        "ultima_atualizacao": datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                                    }
                                    emergencias_encontradas.append(emergencia)
                                    print(f"   ✅ {len(emergencias_encontradas):2d}. {emergencia['evento']} | {emergencia['status']}")
                        except:
                            continue
                except Exception as e:
                    print(f"   ❌ Erro tabela {i+1}: {e}")
                    continue
            
            self.emergencias = emergencias_encontradas
            print(f"✅ {len(self.emergencias)} emergências capturadas!")
            return len(self.emergencias) > 0
            
        except Exception as e:
            print(f"❌ Erro na captura: {e}")
            return False
    
    def salvar_dados(self):
        """Salva os dados capturados em um arquivo JavaScript na pasta Raiz"""
        print("💾 Salvando dados em formato JS compatível...")
        
        try:
            dados_finais = {
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "fonte": "SPIR Monitor AM - Captura Automática Total",
                "url": self.driver.current_url,
                "total_emergencias": len(self.emergencias),
                "emergencias": self.emergencias,
                "metodo": "automatico_com_login"
            }
            
            # Caminho para salvar na raiz externa
            arquivo_js = "../dados_spir.js"
            
            # Transforma os dados em uma variável JavaScript global
            conteudo_js = f"window.dadosSpirDoArquivo = {json.dumps(dados_finais, ensure_ascii=False, indent=2)};"
            
            with open(arquivo_js, 'w', encoding='utf-8') as f:
                f.write(conteudo_js)
            
            print(f"✅ Arquivo gravado com sucesso na RAIZ: {arquivo_js}")
            return "dados_spir.js"
            
        except Exception as e:
            print(f"❌ Erro crítico ao salvar o arquivo JS: {e}")
            return None
    
    def executar_captura_completa(self):
        """Executa todo o processo automaticamente"""
        print("🚀 INICIANDO CAPTURA AUTOMÁTICA TOTAL DO SPIR")
        print("=" * 60)
        
        try:
            print("🔐 CREDENCIAIS DO SPIR:")
            usuario = input("👤 Usuário: ").strip()
            senha = getpass.getpass("🔒 Senha: ").strip()
            
            if not usuario or senha == "":
                print("❌ Credenciais não fornecidas!")
                return False
            
            self.configurar_chrome()
            print("\n🎯 ESTRATÉGIA 1: Tentando acesso direto ao Monitor AM...")
            
            if self.navegar_para_monitor():
                url_atual = self.driver.current_url
                if "login" in url_atual.lower() or self.driver.current_url == "https://spir.cpfl.com.br/":
                    print("🔐 Acesso direto redirecionou para login - fazendo login...")
                    if not self.fazer_login(usuario, senha):
                        return False
                    
                    print("🔄 Tentando Monitor AM novamente após login...")
                    if not self.navegar_para_monitor():
                        return False
                else:
                    if not self.fazer_login(usuario, senha):
                        return False
                    if not self.navegar_para_monitor():
                        return False
            else:
                if not self.fazer_login(usuario, senha):
                    return False
                if not self.navegar_para_monitor():
                    return False
            
            if not self.configurar_filtros_automatico():
                return False
            
            if not self.capturar_emergencias_total():
                print("❌ Nenhuma emergência capturada!")
                return False
            
            arquivo = self.salvar_dados()
            if not arquivo:
                return False
            
            print(f"\n🎉 CAPTURA AUTOMÁTICA CONCLUÍDA COM SUCESSO!")
            print(f"📊 Emergências capturadas: {len(self.emergencias)}")
            return True
            
        except Exception as e:
            print(f"❌ Erro geral no fluxo de execução: {e}")
            return False
        finally:
            if self.driver:
                input("\n⏳ Pressione ENTER para fechar o navegador...")
                self.driver.quit()

def main():
    spir = SPIRAutomatico()
    try:
        sucesso = spir.executar_captura_completa()
        if sucesso:
            print("\n✅ MISSÃO CUMPRIDA!")
        else:
            print("\n❌ FALHA NA MISSÃO")
    except KeyboardInterrupt:
        print("\n⚠️ Operação cancelada")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()