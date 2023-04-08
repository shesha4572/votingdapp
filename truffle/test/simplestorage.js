const Election = artifacts.require("Election");

contract('Election', () => {
  it('should read newly written values', async() => {
    const electionInstance = await Election.deployed();
    var value = (await electionInstance.getPhase()).toNumber();
    assert.equal(value, 0, "0 wasn't the initial value");
    await electionInstance.changeState(1);
    value = (await electionInstance.getPhase()).toNumber();
    assert.equal(value, 1, "0 wasn't the initial value");
  });
});
