// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import "../contracts/SimpleStorage.sol";
// These files are dynamically created at test time
import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";

contract SimpleStorageTest {

  function testWriteValue() public {
    SimpleStorage simpleStorage = SimpleStorage(DeployedAddresses.SimpleStorage());
    simpleStorage.write("hello");
    Assert.equal(simpleStorage.readmessage(), "hello", "Contract should have 1 stored");
    simpleStorage.write("ether");
    Assert.equal(simpleStorage.readmessage(), "ether" , "Contract should have 2 stored");
  }
}
