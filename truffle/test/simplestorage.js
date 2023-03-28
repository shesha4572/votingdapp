const SimpleStorage = artifacts.require("SimpleStorage");

contract('SimpleStorage', () => {
  it('should read newly written values', async() => {
    const simpleStorageInstance = await SimpleStorage.deployed();
    var value = (await simpleStorageInstance.read()).toNumber();

    assert.equal(value, 0, "0 wasn't the initial value");

    await simpleStorageInstance.write("hello");
    value = (await simpleStorageInstance.readmessage()).toString();
    assert.equal(value, "hello", "1 was not written");

    await simpleStorageInstance.write("ethereum");
    value = (await simpleStorageInstance.readmessage()).toString();
    assert.equal(value, "ethereum", "2 was not written");
  });
});
