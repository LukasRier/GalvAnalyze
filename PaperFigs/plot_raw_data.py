# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 20:57:31 2022

@author: Rorym
"""

plt.figure(figsize=(6,5))
for coln in range(neg_count):  
    plt.plot(discharge_cyc_capacities[:,coln],discharge_cyc_potentials[:,coln],
             linewidth=1,color=colors[coln % 10])
    plt.plot(charge_cyc_capacities[:,coln],charge_cyc_potentials[:,coln],
             linewidth=1,color=colors[coln % 10])
plt.xlabel("Capacity / $\mathrm{mAh}$ $\mathrm{g^{-1}}$", fontsize=14)
plt.xticks(fontsize=14)
plt.ylabel("Potential / $\mathrm{V}$", fontsize=14)
plt.yticks(fontsize=14)
ax = plt.gca()
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.035, box.width, box.height * 0.975])
plt.legend(["D1","C1","D2","C2","D3","C3","D4","C4","D5","C5"], loc= 'lower center',
           bbox_to_anchor=(0.5, 1.01), ncol=5)
plt.tight_layout()

if save_dir != None:
    plt.savefig(os.path.join(save_dir,"Capacity vs. Potential (all cycles).png"))
plt.show()