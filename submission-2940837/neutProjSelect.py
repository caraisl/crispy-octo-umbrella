def passes_selection_CC_1_p_0_pi(evt):
    muon_p3mod_cut = (ps.p3mod > 0.1 * ps.unit.GeV) & (ps.p3mod < 1.2 * ps.unit.GeV)
    all_muons = ps.event.all_out_part(evt, ps.pdg.kMuon)
    passing_muons = ps.part.filter(muon_p3mod_cut, all_muons)
    
    proton_p3mod_cut = (ps.p3mod > 0.3 * ps.unit.GeV) & (ps.p3mod < 1 * ps.unit.GeV)
    all_protons = ps.event.all_out_part(evt, ps.pdg.kProton)
    passing_protons = ps.part.filter(proton_p3mod_cut, all_protons)
    # only care about events that have at least one muon with 0.1 <p_mu< 1.2GeV
    if len(passing_muons) < 1:
        return False
    # events must have exactly one proton with 0.3 < p_p < 1 GeV
    elif len(passing_protons) != 1:
        return False
    elif ps.event.all_out_part(evt, ps.pdg.kPiZero) != []:
        return False
    elif ps.part.filter(ps.p3mod > 70 * ps.unit.MeV, ps.event.all_out_part(evt, ps.pdg.kPiMinus)) !=[]: # no charged pions with p>70 MeV
        return False
    elif ps.part.filter(ps.p3mod > 70 * ps.unit.MeV, ps.event.all_out_part(evt, ps.pdg.kPiPlus)) !=[]:  # no charged pions with p>70 MeV
        return False
    elif ps.part.filter((ps.p3mod < 0.1 * ps.unit.GeV),ps.event.all_out_part(evt, ps.pdg.kMuon)) != [] or ps.part.filter( (ps.p3mod > 2 * ps.unit.GeV),ps.event.all_out_part(evt, ps.pdg.kMuon)) != []:
        return False
    return True

def passes_selection_CC_0_pi(evt):
    # only care about events that has exactly 1 outgoing muon
    if not ps.event.has_exact_out_part(evt, ps.pdg.kMuon, 1):
        return False
    elif ps.event.all_out_part(evt, ps.pdg.kPiZero) != []:
        return False
    elif ps.part.filter(ps.p3mod > 70 * ps.unit.MeV, ps.event.all_out_part(evt, ps.pdg.kPiMinus)) !=[]: # no charged pions with p>70 MeV
        return False
    elif ps.part.filter(ps.p3mod > 70 * ps.unit.MeV, ps.event.all_out_part(evt, ps.pdg.kPiPlus)) !=[]:  # no charged pions with p>70 MeV
        return False
    elif ps.part.filter((ps.p3mod < 0.1 * ps.unit.GeV),ps.event.all_out_part(evt, ps.pdg.kMuon)) != [] or ps.part.filter( (ps.p3mod > 2 * ps.unit.GeV),ps.event.all_out_part(evt, ps.pdg.kMuon)) != []:
        return False
    return True

def projection_p_mu(evt):
    # grab the muon particle object
    muon = ps.event.hm_out_part(evt, ps.pdg.kMuon)
    # get its momentum in GeV/c
    return ps.p3mod(muon) / ps.unit.GeV_c

def projection_cos_theta_mu(evt):
    muon = ps.event.hm_out_part(evt, ps.pdg.kMuon)
    return ps.costheta(muon)

def projection_e_cal(evt):
    # grab the muon particle object
    muon = ps.event.hm_out_part(evt, ps.pdg.kMuon)
    all_protons = ps.event.all_out_part(evt, ps.pdg.kProton)
    # get its momentum in GeV/c
    # definition of E_cal given https://journals.aps.org/prd/abstract/10.1103/PhysRevD.108.053002#s4
    return (ps.energy(muon) + sum([ps.kinetic_energy(proton) for proton in all_protons]) +0.04) / ps.unit.GeV