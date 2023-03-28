// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract SimpleStorage {
  uint256 value;
  string message;

  function read() public view returns (uint256) {
    return value;
  }

  function readmessage() public view returns (string memory){
    return message;
  }


  function write(string memory newValue) public {
    message = newValue;
  }
}
