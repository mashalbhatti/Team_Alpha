import smartpy as sp

@sp.module
def main():
    class BuyLifeInsurance(sp.Contract):
        def __init__(self, insurer):
            self.data.insurer = insurer 
            self.data.insured = sp.address("")
            self.data.policyholder = sp.address("")
            self.data.premium = sp.tez(0)
            self.data.deathBenefit = sp.tez(0)
            self.data.beneficiaries = sp.list(t=sp.TMap(tkey=sp.TAddress, tvalue=sp.int)) 
            self.data.isActive = False  

        @sp.entrypoint
        def createInsurancePolicy(self, insured, policyholder, premium, death_benefit, beneficiaries, is_active):
            assert (
                sp.sender == self.data.insurer
            ), "The endpoint can only be called by the insurer." 

            self.data.insured = insured
            self.data.policyholder = policyholder
            self.data.premium = premium
            self.data.deathBenefit = death_benefit
            self.data.beneficiaries = [sp.big_map(l={beneficiary: percentage}) for beneficiary, percentage in beneficiaries]
            self.data.isActive = is_active 
            
        @sp.entrypoint
        def updateInsurancePolicy(self):
            assert (
                sp.sender == self.data.insurer
            ), "The endpoint can only be called by the insurer."

if "main" in __name__:
    @sp.add_test()
    def basic_scenario(): 
        # Define test accounts
        insurer = sp.test_account("insurer")
        insured = sp.test_account("insured")
        policyholder = sp.test_account("policyholder")
        beneficiary1 = sp.test_account("beneficiary1")
        beneficiary2 = sp.test_account("beneficiary2")
        beneficiaries = [(beneficiary1.address, 30), (beneficiary2.address, 70)]
        premium = sp.tez(1000)
        death_benefit = sp.tez(10000)
        is_active = True
    
        # Test entrypoints: createInsurancePolicy and updateInsurancePolicy
        scenario = sp.test_scenario("Test createInsurancePolicy and updateInsurancePolicy", main)
    
        # Initialize contract
        contract = main.BuyLifeInsurance(insurer.address)
        scenario += contract
    
        # Test entrypoint: createInsurancePolicy
        scenario.h1("Test createInsurancePolicy")
        scenario += contract.createInsurancePolicy(
            insured=insured.address,
            policyholder=policyholder.address,
            premium=premium,
            death_benefit=death_benefit,
            beneficiaries=beneficiaries,
            is_active=is_active,
            _sender=insurer
        )

        # Attempt to call createInsurancePolicy from non-insurer account
        with scenario:
            scenario.h1("Test createInsurancePolicy from non-insurer account")
            scenario += contract.createInsurancePolicy(
                insured=insured.address,
                policyholder=policyholder.address,
                premium=premium,
                death_benefit=death_benefit,
                beneficiaries=beneficiaries,
                is_active=is_active,
                _sender=insured,
                _valid=False,
                _exception="The endpoint can only be called by the insurer."
            )

        # Test entrypoint: updateInsurancePolicy
        scenario.h1("Test updateInsurancePolicy")
        scenario += contract.updateInsurancePolicy(_sender=insurer)

        # Attempt to call updateInsurancePolicy from non-insurer account
        with scenario:
            scenario.h1("Test updateInsurancePolicy from non-insurer account")
            scenario += contract.updateInsurancePolicy(
                _sender=insured,
                _valid=False,
                _exception="This entrypoint can only be called by the insurer."
            )