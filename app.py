
import subprocess
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from json2html import json2html

app = Flask(__name__)
CORS(app)

def check_tool_availability(tool_name):
    try:
        result = subprocess.run(
            ['where' if os.name == 'nt' else 'which', tool_name],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        return result.returncode == 0
    except Exception:
        return False

def run_command(command_list, output_file=None):
    try:
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=300
        )
        
        if result.returncode != 0:
            return f"❌ Error:\n{result.stderr.strip()}\n{result.stdout.strip()}"

        if output_file:
            try:
                with open(output_file, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                    return content if content else "⚠️ Empty report generated."
            except FileNotFoundError:
                return f"❌ Report file not found: {output_file}"

        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "⏰ Error: Analysis timed out."
    except Exception as e:
        return f"❌ Execution exception: {str(e)}"
    
def run_commandgitleaks(command, output_file=None, cwd=None):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd  
        )

        if output_file and os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return result.stdout or result.stderr
    except Exception as e:
        return f"⚠️ Erreur lors de l'exécution : {str(e)}"

def run_nikto(target):
    nikto_path = 'C:/Users/adam/Desktop/py/tools/nikto/program/nikto.pl'
    
    # Corriger les formats mal formés comme "http:/..." ou "https:/..."
    target = target.strip().replace('\\', '/')
    if target.startswith("http:/") and not target.startswith("http://"):
     target = target.replace("http:/", "http://", 1)
    elif target.startswith("https:/") and not target.startswith("https://"):
     target = target.replace("https:/", "https://", 1)
    
    if not os.path.exists(nikto_path):
        return "⚠️ Nikto not found at specified path."
    return run_command(['perl', nikto_path, '-h', target, '-output', 'nikto_report.html'], 'nikto_report.html')

def run_ffuf(target):
    import re
    ffuf_path = 'C:/Users/adam/Desktop/py/tools/ffuf/ffuf.exe'
    wordlist = 'C:/Users/adam/Desktop/py/worldlist.txt'
    output = 'ffuf_report.html'

    if not os.path.exists(ffuf_path):
        return "⚠️ FFUF not found at specified path."
    if not os.path.exists(wordlist):
        return "❌ Wordlist missing."
    
    print(f"Target reçu : {target}")
   # Nettoyage du target
    target = target.strip().replace('\\', '/')

   # Corriger les formats mal formés comme "http:/..." ou "https:/..."
    target = target.strip().replace('\\', '/')
    if target.startswith("http:/") and not target.startswith("http://"):
      target = target.replace("http:/", "http://", 1)
    elif target.startswith("https:/") and not target.startswith("https://"):
     target = target.replace("https:/", "https://", 1)

    #  Vérifie si l'URL est bien formée
    from urllib.parse import urlparse
    parsed = urlparse(target)
    if not parsed.scheme or not parsed.netloc:
        return f"❌ Invalid URL format: {target}"

    # 🔍 Construire l'URL pour FFUF
    url = f"{target.rstrip('/')}/FUZZ"
    cmd = [ffuf_path, '-u', url, '-w', wordlist, '-of', 'html', '-o', output]
    return run_command(cmd, output)

def run_gitleaks(target):
    gitleaks_path = 'C:/Users/adam/Desktop/py/tools/gitleaks/gitleaks.exe'
    report_path = os.path.join(os.path.dirname(gitleaks_path), 'gitleaks_report.json')
    print(f"Target reçu : {target}")

    if not os.path.exists(gitleaks_path):
        return "⚠️ Gitleaks not available."

    result = run_commandgitleaks(
        [
            gitleaks_path,
            'detect',
            '--source', target,
            '--no-git',  # <-- ajout essentiel pour scanner les fichiers non commités
            '--report-format', 'json',
            '--report-path', report_path
        ],
        'gitleaks_report.json',
        cwd=os.path.dirname(gitleaks_path)
    )

    if os.path.exists(report_path):
        with open(report_path, 'r', encoding='utf-8') as f:
            data = f.read().strip()
            if not data or data == '[]':
                return "✅ Aucune fuite détectée par Gitleaks."
            else:
                return data  # ou json.loads(data) selon ton besoin

    return "⚠️ Rapport introuvable."



def run_semgrep(target):
    if not check_tool_availability('semgrep'):
        return "⚠️ Semgrep not installed."

    try:
        result = subprocess.run(
            ['semgrep', '--config', 'auto', '--json', target],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode != 0:
            return f"❌ Semgrep error:\n{result.stderr.strip()}\n{result.stdout.strip()}"
        
        try:
            result_dict = json.loads(result.stdout)
            html_report = json2html.convert(json=result_dict)
            html_file = 'semgrep_report.html'
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_report)
            return f"✅ Semgrep report generated: {html_file}"
        except json.JSONDecodeError:
            return f"❌ Invalid JSON output from Semgrep\nRaw output: {result.stdout[:500]}..."
    except Exception as e:
        return f"❌ Exception while running Semgrep: {str(e)}"

def run_trufflehog(target):
    if not check_tool_availability('trufflehog'):
        return "⚠️ TruffleHog not available."
    return run_command(['trufflehog', 'git', 'file://' + target, '--json'], 'trufflehog_report.json')

def launch_zap_gui():
    zap_exe = 'C:/Users/adam/Desktop/py/tools/Zed Attack Proxy/ZAP.exe'
    if not os.path.exists(zap_exe):
        return "❌ ZAP.exe not found."
    try:
        subprocess.Popen([zap_exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "✅ ZAP GUI launched successfully."
    except Exception as e:
        return f"❌ Failed to launch ZAP GUI: {str(e)}"

def launch_burp_suite_gui():
    burp_exe = 'C:/Users/adam/Desktop/py/tools/BurpSuitePro/BurpSuitePro.exe'
    if not os.path.exists(burp_exe):
        return "❌ BurpSuitePro.exe not found."
    try:
        subprocess.Popen([burp_exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "✅ Burp Suite launched successfully."
    except Exception as e:
        return f"❌ Failed to launch Burp Suite: {str(e)}"

@app.route('/api/vulnerability/execute', methods=['POST'])
def execute_vulnerability():
    data = request.get_json()
    app.logger.debug(f"📥 Request received: {data}")

    if not data:
        return jsonify({'status': 'error', 'message': '❌ No data received.'}), 400

    tool = data.get('tool')
    target = data.get('target', '').strip()

    if not tool:
        return jsonify({'status': 'error', 'message': '❌ No tool specified.'}), 400

    if not target:
        return jsonify({'status': 'error', 'message': '❌ Target/repo path is required.'}), 400

    # Normalize Windows paths
    target = os.path.normpath(target)

    result = ""
    try:
        if tool == 'Nikto':
            result = run_nikto(target)
        elif tool == 'FFUF':
            result = run_ffuf(target)
        elif tool == 'Gitleaks':
            result = run_gitleaks(target)
        elif tool == 'Semgrep':
            result = run_semgrep(target)
        elif tool == 'TruffleHog':
            result = run_trufflehog(target)
        elif tool == 'OWASP ZAP':
            result = launch_zap_gui()
        elif tool == 'Burp Suite':
            result = launch_burp_suite_gui()
        else:
            return jsonify({'status': 'error', 'message': f"❌ Unsupported tool: {tool}"}), 400

        app.logger.debug(f"📤 {tool} result: {result[:1000]}")
        return jsonify({'status': 'success', 'output': result})
    except Exception as e:
        app.logger.error(f"❌ Error executing {tool}: {str(e)}")
        return jsonify({'status': 'error', 'message': f"❌ Error executing {tool}: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
