import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Kullanılacak Dağılımların Listesi
DISTRIBUTIONS = [
    stats.norm,  # Normal Dağılımı
    stats.expon,  # Üstel Dağılım (Exponential)
    stats.poisson,  # Poisson Dağılımı
    stats.binom,  # Binom Dağılımı
    stats.bernoulli,  # Bernoulli Dağılımı
    stats.uniform,  # Tekdüze Dağılım (Uniform)
    stats.gamma,  # Gamma Dağılımı
    stats.beta,  # Beta Dağılımı
    stats.lognorm,  # Log-Normal Dağılımı
    stats.chi2,  # Ki-Kare Dağılımı (Chi-Squared)
    stats.weibull_min,  # Weibull Dağılımı (Minimum Formu)
    stats.weibull_max,  # Weibull Dağılımı (Maksimum Formu)
    stats.pareto,  # Pareto Dağılımı
    stats.t  # Student's t-Dağılımı
]

def evaluate_distributions(data):
    results = []
    for dist in DISTRIBUTIONS:
        try:
            params = dist.fit(data)
            
            # Anderson-Darling Testi
            ad_stat, ad_critical, ad_significance = stats.anderson(data, dist=dist.name)
            
            # Kolmogorov-Smirnov Testi
            ks_stat, ks_p_value = stats.kstest(data, dist.name, args=params)
            
            results.append({
                'distribution': dist.name,
                'parameters': params,
                'anderson_statistic': ad_stat,
                'critical_values': ad_critical,
                'significance_level': ad_significance,
                'kolmogorov_smirnov_statistic': ks_stat,
                'kolmogorov_smirnov_p_value': ks_p_value
            })
        except Exception as e:
            results.append({
                'distribution': dist.name,
                'error': str(e)
            })
    return results

def sort_distributions(results):
    filtered_results = [res for res in results if 'kolmogorov_smirnov_p_value' in res]
    sorted_results = sorted(filtered_results, key=lambda x: x['kolmogorov_smirnov_p_value'], reverse=True)
    return sorted_results

def visualize_best_fits(data, results, top_n=3):
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=30, density=True, alpha=0.6, color='gray', label='Veri Dağılımı')
    
    for i, result in enumerate(results[:top_n]):
        dist_name = result['distribution']
        params = result['parameters']
        
        x_values = np.linspace(min(data), max(data), 1000)
        
        if hasattr(stats, dist_name):
            dist = getattr(stats, dist_name)
            pdf = dist.pdf(x_values, *params)
            
            plt.plot(x_values, pdf, label=f'{dist_name} uyumu', linewidth=2)
    
    plt.xlabel('Değer')
    plt.ylabel('Yoğunluk')
    plt.title('En Uyumlu Dağılımların Gösterimi')
    plt.legend()
    plt.show()

def main():
    # Rastgele veri üretimi
    data = np.random.normal(loc=0, scale=1, size=1000)
    
    # Dağılımları Değerlendir
    fit_results = evaluate_distributions(data)
    
    # Dağılımları Sıralama
    ranked_results = sort_distributions(fit_results)
    
    # En iyi uyan dağılımları yazdır
    print("\nKolmogorov-Smirnov p-değerine göre en uyumlu dağılımlar:\n")
    for i, result in enumerate(ranked_results[:5]):  
        print(f"{i+1}. Dağılım: {result['distribution']}")
        print(f"   KS İstatistiği: {result['kolmogorov_smirnov_statistic']}")
        print(f"   KS p-Değeri: {result['kolmogorov_smirnov_p_value']}")
        print(f"   Anderson-Darling İstatistiği: {result['anderson_statistic']}")
        print(f"   Parametreler: {result['parameters']}\n")
    
    # En iyi uyum gösteren dağılımların grafiği
    visualize_best_fits(data, ranked_results, top_n=3)

if __name__ == "__main__":
    main()
