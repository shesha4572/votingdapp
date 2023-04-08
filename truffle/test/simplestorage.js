const Election = artifacts.require("Election");

contract('Election', () => {
  it('should read newly written values', async() => {
    const electionInstance = await Election.deployed();
    var value = (await electionInstance.getContestantCount()).toNumber();
    assert.equal(value, 0, "0 wasn't the initial value");
    await electionInstance.addContestant("Modi");
    var count = (await electionInstance.getContestantCount()).toNumber();
    assert.equal(count, 1, "0 wasn't the initial value");
    var phase = (await electionInstance.getPhase())
    assert.equal(phase , 0 , phase + "wrong");
  });
});
