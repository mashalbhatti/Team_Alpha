<script>
  import { BeaconWallet } from "@taquito/beacon-wallet";
  import { NetworkType } from "@airgap/beacon-types";
  import { TezosToolkit } from "@taquito/taquito";

  const rpcUrl = "https://ghostnet.tezos.marigold.dev"; 
  const Tezos = new TezosToolkit(rpcUrl);
  const contractAddress = "KT1R4i4qEaxF7v3zg1M8nTeyrqk8JFmdGLuu"; //TODO: change this address

  let wallet;
  let address;
  let balance;

  let depositAmount = 1;
  let ButtonActive = false;
  let ButtonActiveLabel = "Activate the contract";

  let withdrawButtonActive = true;
  let withdrawButtonLabel = "Withdraw";

  let confirmMessage = "";  


  const connectWallet = async () => {
    const newWallet = new BeaconWallet({
      name: "Simple dApp tutorial",
      network: {
        type: NetworkType.GHOSTNET,
      },
    });
    await newWallet.requestPermissions();
    address = await newWallet.getPKH();
    wallet = newWallet;
    ButtonActive = true;
  };

  const disconnectWallet = () => {
    wallet.client.clearActiveAccount();
    wallet = undefined;
  };

  const call = async () => {
    ButtonActive = false;
    ButtonActiveLabel = "Processing...";

    Tezos.setWalletProvider(wallet);
    const contract = await Tezos.wallet.at(contractAddress);

    //TODO: write the right way to call the contract

    const transactionParams = await contract.methods
      .deposit()
      .toTransferParams({
        amount: depositAmount,
      });
    const estimate = await Tezos.estimate.transfer(transactionParams);

    const operation = await Tezos.wallet
      .transfer({
        ...transactionParams,
        ...estimate,
      })
      .send();

    console.log(`Waiting for ${operation.opHash} to be confirmed...`);

    await operation.confirmation(2);

    console.log(
      `Operation injected: https://ghost.tzstats.com/${operation.opHash}`
    );

    ButtonActive = true;
    ButtonActiveLabel = "activate the contract";

    confirmMessage = "contract have beeen activated!";

    setTimeout(() => {
      confirmMessage = "";
    }, 3000);

  };

  const checkAddressValidity = (input) => {
    // Regular expression to match a Tezos contract or address
    const tezosRegex = /^(KT1|tz1|tz2|tz3)[1-9A-HJ-NP-Za-km-z]{33}$/;
    return tezosRegex.test(input);
  };
</script>

<main>
  <div>
    <h1>Insurance manager</h1>
    <div class="card">
      {#if wallet}
        <p>
          Insurance contract address :
          <input type="text" bind:value={depositAmount} />
        </p>
        <p>
          <button on:click={disconnectWallet}> Disconnect wallet </button>
          <button on:click={call} disabled={!ButtonActive}>
            {ButtonActiveLabel}
          </button>
        </p>
      {:else}
        <button on:click={connectWallet}> Connect wallet </button>
      {/if}
    </div>
  </div>
</main>

<style>
</style>
