# Gerekli kütüphaneleri içe aktar
import re
import networkx as nx

# FSM dosyasını okuyan fonksiyon
def load_fsm_from_file(file_path):
    # Verilen bir dosya yolundan FSM formatındaki veriyi okur ve metin olarak döndürür
    with open(file_path, 'r') as file:
        fsm_data = file.read()
    return fsm_data

# FSM verisini regex ile çözümleyen fonksiyon
def parse_fsm_data(fsm_data):
    # FSM verisini regex ile çözümleyerek FSM'in yapısını çıkarır
    
    # Geçişler için desen
    transition_pattern = r"(\d+)\s+(\w+)\s+(\w+)\s+(\d+)"
    transitions = re.findall(transition_pattern, fsm_data)
    
    # FSM parametrelerini çekme
    inputs = int(re.search(r"\.i\s+(\d+)", fsm_data).group(1))
    outputs = int(re.search(r"\.o\s+(\d+)", fsm_data).group(1))
    states = int(re.search(r"\.s\s+(\d+)", fsm_data).group(1))
    products = int(re.search(r"\.p\s+(\d+)", fsm_data).group(1))
    reset_state = re.search(r"\.r\s+(\w+)", fsm_data).group(1)
    
    # FSM yapısını oluşturma
    fsm_structure = {
        "inputs": inputs,
        "outputs": outputs,
        "states": states,
        "products": products,
        "reset_state": reset_state,
        "transitions": [
            {"input": int(t[0]), "current_state": t[1], "next_state": t[2], "output": int(t[3])} 
            for t in transitions
        ]
    }
    
    return fsm_structure

# Euler yolu kontrol fonksiyonu
def check_eulerian_path(fsm_structure):
    # FSM'deki tüm geçişlerin bir Euler yolu oluşturup oluşturmadığını kontrol eder
    
    # Geçişleri grafa ekle
    G = nx.DiGraph()
    for transition in fsm_structure['transitions']:
        G.add_edge(transition['current_state'], transition['next_state'])
    
    # Euler yolu var mı kontrol et
    has_euler_path = nx.is_eulerian(G)
    
    return has_euler_path

# En uzun yolu bulan ve tüm kenarları kapsayan fonksiyon
def find_longest_path(fsm_structure):
    # FSM'deki en uzun yolu bulur ve bu yolun tüm kenarları kapsayıp kapsamadığını kontrol eder
    
    # Geçişleri grafa ekle
    G = nx.DiGraph()
    for transition in fsm_structure['transitions']:
        G.add_edge(transition['current_state'], transition['next_state'])
    
    # En uzun yolu bulmaya çalış
    try:
        longest_path = nx.dag_longest_path(G)
        longest_path_edges = [(longest_path[i], longest_path[i+1]) for i in range(len(longest_path) - 1)]
    except nx.NetworkXUnfeasible:
        return False, []
    
    # Tüm kenarların kapsanıp kapsanmadığını kontrol et
    all_edges = list(G.edges())
    
    all_edges_covered = all(edge in longest_path_edges for edge in all_edges)
    
    return all_edges_covered, longest_path

# Ana işlev, kullanıcıdan dosya yolunu alır ve FSM analizi yapar
def main():
    # Ana işlev, kullanıcıdan dosya yolunu alır ve FSM analizi yapar
    
    # Dosya yolunu al
    file_path = input("FSM dosyasının yolunu giriniz: ")
    
    # FSM verisini yükle
    fsm_data = load_fsm_from_file(file_path)
    
    # FSM yapısını çözümlə
    fsm_structure = parse_fsm_data(fsm_data)
    print("FSM Yapısı:", fsm_structure)
    
    # Euler yolu kontrolü yap
    euler_path_exists = check_eulerian_path(fsm_structure)
    print("Euler yolu mevcut mu?:", euler_path_exists)
    
    # En uzun yol kontrolü yap
    edges_covered, longest_path = find_longest_path(fsm_structure)
    print("En uzun yol tüm kenarları kapsıyor mu?:", edges_covered)
    print("En uzun yol:", longest_path)

# Ana fonksiyonu çalıştır
if __name__ == "__main__":
    main()
