import matplotlib.pyplot as plt


perf_objrel_nounpp_SP = 0.04
perf_objrel_nounpp_PS = 0.04

perf_objrel_PS = 0.64
perf_objrel_SP = 0.53

perf_embedding_mental_LR_SPS = 0.92
perf_embedding_mental_LR_PSP = 0.99

perf_embedding_mental_SR_SP = 0.986
perf_embedding_mental_SR_PS = 0.99

SR_nested = (perf_objrel_PS + perf_objrel_SP)/2
SR_successive = (perf_embedding_mental_SR_SP + perf_embedding_mental_SR_PS)/2
LR_nested = (perf_objrel_nounpp_SP + perf_objrel_nounpp_PS)/2
LR_successive = (perf_embedding_mental_LR_SPS + perf_embedding_mental_LR_PSP)/2

fig, ax = plt.subplots(figsize=(10, 10))
ax.plot((SR_successive, LR_successive), marker='^', markersize=10, ls='-', color='k', lw=2, label='Short-range')
ax.plot((LR_successive, LR_nested), marker='D', markersize=10, ls='--', color='b', lw=2, label='Long-range')
ax.set_xticks((0,1))
ax.set_xticklabels(('Successive', 'Nested'), fontsize=16)
ax.set_xlim((-0.2, 1.2))
ax.set_xlabel('LR-mechanism free/occupied', fontsize=18)
ax.set_ylabel('Model accuracy on V2', fontsize=18)
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.subplots_adjust(right=0.75)
plt.savefig('../../Figures/interaction_nested_SR_LR.png')