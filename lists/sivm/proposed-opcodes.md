All Proposed Opcodes
--------------------

All SIP proposed opcodes that have not shipped. This includes all
unshipped SIPs, even withdrawn and non-viable proposals.

| SIP                                                                    | Opcode | Name               | Description                                                                  |
|------------------------------------------------------------------------|--------|--------------------|------------------------------------------------------------------------------|
| [101](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-101.md)                          | 0x5C   | tx.gas             | primordial account-abstraction support                                       |
| [141](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-141.md)                          | 0xFE   | INVALID/ABORT      | Designated invalid opcode. <br />(Adopted in practice, Not formally adopted) |
| [615](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-615.md)                          | 0xB0   | JUMPTO             | static jump                                                                  |
| [615](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-615.md)                          | 0xB1   | JUMPIF             | static conditional jump                                                      |
| [615](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-615.md)                          | 0xB2   | JUMPV              | static jump table                                                            |
| [615](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-615.md)                          | 0xB3   | JUMPSUB            | static subroutine call                                                       |
| [615](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-615.md)                          | 0xB4   | JUMPSUBV           | static subroutine table call                                                 |
| [615](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-615.md)                          | 0xB5   | BEGINSUB           | marker opcode                                                                |
| [615](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-615.md)                          | 0xB6   | BEGINDATA          | marker opcode                                                                |
| [615](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-615.md)                          | 0xB7   | RETURNSUB          | subroutine return                                                            |
| [615](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-615.md)                          | 0xB8   | PUTLOCAL           | call local storage                                                           |
| [615](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-615.md)                          | 0xB9   | GETLOCAL           | call local storage                                                           |
| [663](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-663.md)                          | 0xE6   | DUPN               | Unlimited dup                                                                |
| [663](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-663.md)                          | 0xE7   | SWAPN              | Unlimited swap                                                               |
| [663](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-663.md)                          | 0xE8   | EXCHANGE           | Deep swap                                                                    |
| [698](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-698.md)                          | 0x46   | BLOCKREWARD        | Get the block reward for the current block                                   |
| [1109](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-1109.md)                        | 0xFB   | PRECOMPILEDCALL    | call only precompiled addresses                                              |
| [1153](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-1153.md)                        | 0xB3   | TLOAD              | Transient data load                                                          |
| [1153](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-1153.md)                        | 0xB4   | TSTORE             | Transient data store                                                         |
| [2315](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-2315.md)                        | 0x5E   | RETURNSUB          | Subroutine return                                                            |
| [2315](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-2315.md)                        | 0x5F   | RJUMPSUB           | Subroutine jump                                                              |
| [2327](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-2327.md)                        | 0xB6   | BEGINDATA          | End of executable code marker                                                |
| [2330](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-2330.md)                        | 0x5C   | EXTSLOAD           | Load external contract data                                                  |
| [2936](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-2936.md)                        | 0x5C   | EXTCLEAR           | Split storage clearing form SELFDESTRUCT                                     |
| [2937](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-2937.md)                        | 0xA8   | SET_INDESTRUCTABLE | Prevents future SELFDESTRUCTs                                                |
| [2938](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-2938.md)                        | 0x48   | NONCE              | Get the nonce of the callee                                                  |
| [2938](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-2938.md)                        | 0x49   | PAYGAS             | Pays gas for all further operations                                          |
| [2970](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-2970.md)                        | 0x4A   | IS_STATIC          | Is current frame static?                                                     |
| [2997](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-2997.md)                        | 0xF6   | IMPERAONATECALL    | Call with sender calculated from salt and caller                             |
| [3074](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3074.md)                        | 0xF6   | AUTH               | Preparatory operation for AUTHCALL                                           |
| [3074](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3074.md)                        | 0xF7   | AUTHCALL           | Call with callee set to externally owned account                             |
| [3322](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3322.md)                        | 0x49   | SELFGAS            | Store gas refund to account                                                  |
| [3322](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3322.md)                        | 0x49   | USEGAS             | Increase execution gas from account stored gas                               |
| [3322](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3322.md)                        | 0x49   | STOREGAS           | Move gas to refund                                                           |
| [3332](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3332.md)                        | 0x46   | MEDGASPRICE        | Get median gas price of prior block                                          |
| [3337](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3337.md)                        | 0x5C   | SETFP              | Sets a frame pointer to a memory location                                    |
| [3337](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3337.md)                        | 0x5D   | GETFP              | Gets the current frame pointer                                               |
| [3337](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3337.md)                        | 0x5E   | MLOADFP            | Reads memory at the frame pointer                                            |
| [3337](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3337.md)                        | 0x5F   | MSTOREFP           | Writes memory at the frame pointer                                           |
| [3455](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3455.md)                        | 0xF8   | SUDO               | Unvalidated AUTHCALL (april fools joke)                                      |
| [3508](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3508.md)                        | 0x47   | ORIGINDATALOAD     | Load transaction calldata                                                    |
| [3508](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3508.md)                        | 0x48   | ORIGINDATASIZE     | Size of transaction calldata                                                 |
| [3508](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3508.md)                        | 0x49   | ORIGINDATACOPY     | Bulk load transaction calldata                                               |
| [3520](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3520.md)                        | 0x4A   | ENTRYPOINT         | To address of transaction                                                    |
| [4200](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-4200.md)                        | 0xE0   | RJUMP              | relative jump                                                                |
| [4200](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-4200.md)                        | 0xE1   | RJUMPI             | relative conditional jump                                                    |
| [4200](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-4200.md)                        | 0xE2   | RJUMPV             | relative jump table                                                          |
| [4520](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-4520.md)                        | 0xEB   | -                  | Reserve for multi-byte opcodes                                               |
| [4520](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-4520.md)                        | 0xEC   | -                  | Reserve for multi-byte opcodes                                               |
| [4750](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-4750.md)                        | 0xE3   | CALLF              | EOF Subroutine Call                                                          |
| [4750](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-4750.md)                        | 0xE4   | RETF               | EOF Subroutine return                                                        |
| [4788](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-4788.md)                        | 0x4A   | BEACON_ROOT        | Exposes the Beacon Chain Root                                                |
| [4844](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-4844.md)                        | 0x49   | BLOBHASH           | Returns hashes of blobs in the transaction                                   |
| [5000](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-5000.md)                        | 0x1E   | MULDIV             | combo multiply then divide trinary operation                                 |
| [5003](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-5003.md)                        | 0xF8   | AUTHUSURP          | Adds code into EOAs                                                          |
| [5478](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-5478.md)                        | 0xF6   | CREATE2COPY        | Create 2 with no initcode and contract copying                               |
| [5656](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-5656.md)                        | 0xB7   | MCOPY              | Memory copy                                                                  |
| [5920](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-5920.md)                        | 0xF9   | PAY                | transfers value from caller to target                                        |
| [6206](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-6206.md)                        | 0xE5   | JUMPF              | EOF Function Jump                                                            |
| [6888](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-6888.md)                        | 0x5B   | JUMPC              | Jump if the most recent arithmetic op set the carry bit                      |
| [6888](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-6888.md)                        | 0x5C   | JUMPO              | Jump if the most recent arithmetic op set the overflow bit                   |
| [6913](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-6913.md)                        | 0x49   | SETCODE            | Replace code of current contract                                             |
| [SIP-7069](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7069.md)                    | 0xF7   | RETURNDATALOAD     | Loads data returned from a call to the stack                                 |
| [SIP-7069](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7069.md)                    | 0xF8   | EXTCALL            | CALL without gas and output memory                                           |
| [SIP-7069](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7069.md)                    | 0xF9   | EXTDELEGATECALL    | DELEGATECALL without gas and output memory                                   |
| [SIP-7069](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7069.md)                    | 0xFB   | EXTSTATICCALL      | STATICCALL without gas and output memory                                     |
| [SIP-7480](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7480.md)                    | 0xD0   | DATALOAD           | Loads data from EOF data section, via stack                                  |
| [SIP-7480](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7480.md)                    | 0xD1   | DATALOADN          | Loads data from EOF data section, via immediate                              |
| [SIP-7480](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7480.md)                    | 0xD2   | DATASIZE           | Size of the EOF data section                                                 |
| [SIP-7480](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7480.md)                    | 0xD3   | DATACOPY           | Bulk data section copy                                                       |
| [SIP-7620](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7620.md)                    | 0xEC   | EOFCREATE          | Create from EOF contained initcode                                           |
| [SIP-7620](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7620.md)                    | 0xED   | TXCREATE           | Create from transaction contained initcode (removed from SIP-7620)           |
| [SIP-7620](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7620.md)                    | 0xEE   | RETURNCONTRACT     | Contract to be created, references EOF data                                  |
