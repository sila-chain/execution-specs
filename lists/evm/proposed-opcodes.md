All Proposed Opcodes
--------------------

All SIP proposed opcodes that have not shipped. This includes all
unshipped SIPs, even withdrawn and non-viable proposals.

| SIP                                                                    | Opcode | Name               | Description                                                                  |
|------------------------------------------------------------------------|--------|--------------------|------------------------------------------------------------------------------|
| [101](https://sips.sila.org/SIPS/sip-101)                          | 0x5C   | tx.gas             | primordial account-abstraction support                                       |
| [141](https://sips.sila.org/SIPS/sip-141)                          | 0xFE   | INVALID/ABORT      | Designated invalid opcode. <br />(Adopted in practice, Not formally adopted) |
| [615](https://sips.sila.org/SIPS/sip-615)                          | 0xB0   | JUMPTO             | static jump                                                                  |
| [615](https://sips.sila.org/SIPS/sip-615)                          | 0xB1   | JUMPIF             | static conditional jump                                                      |
| [615](https://sips.sila.org/SIPS/sip-615)                          | 0xB2   | JUMPV              | static jump table                                                            |
| [615](https://sips.sila.org/SIPS/sip-615)                          | 0xB3   | JUMPSUB            | static subroutine call                                                       |
| [615](https://sips.sila.org/SIPS/sip-615)                          | 0xB4   | JUMPSUBV           | static subroutine table call                                                 |
| [615](https://sips.sila.org/SIPS/sip-615)                          | 0xB5   | BEGINSUB           | marker opcode                                                                |
| [615](https://sips.sila.org/SIPS/sip-615)                          | 0xB6   | BEGINDATA          | marker opcode                                                                |
| [615](https://sips.sila.org/SIPS/sip-615)                          | 0xB7   | RETURNSUB          | subroutine return                                                            |
| [615](https://sips.sila.org/SIPS/sip-615)                          | 0xB8   | PUTLOCAL           | call local storage                                                           |
| [615](https://sips.sila.org/SIPS/sip-615)                          | 0xB9   | GETLOCAL           | call local storage                                                           |
| [663](https://sips.sila.org/SIPS/sip-663)                          | 0xE6   | DUPN               | Unlimited dup                                                                |
| [663](https://sips.sila.org/SIPS/sip-663)                          | 0xE7   | SWAPN              | Unlimited swap                                                               |
| [663](https://sips.sila.org/SIPS/sip-663)                          | 0xE8   | EXCHANGE           | Deep swap                                                                    |
| [698](https://sips.sila.org/SIPS/sip-698)                          | 0x46   | BLOCKREWARD        | Get the block reward for the current block                                   |
| [1109](https://sips.sila.org/SIPS/sip-1109)                        | 0xFB   | PRECOMPILEDCALL    | call only precompiled addresses                                              |
| [1153](https://sips.sila.org/SIPS/sip-1153)                        | 0xB3   | TLOAD              | Transient data load                                                          |
| [1153](https://sips.sila.org/SIPS/sip-1153)                        | 0xB4   | TSTORE             | Transient data store                                                         |
| [2315](https://sips.sila.org/SIPS/sip-2315)                        | 0x5E   | RETURNSUB          | Subroutine return                                                            |
| [2315](https://sips.sila.org/SIPS/sip-2315)                        | 0x5F   | RJUMPSUB           | Subroutine jump                                                              |
| [2327](https://sips.sila.org/SIPS/sip-2327)                        | 0xB6   | BEGINDATA          | End of executable code marker                                                |
| [2330](https://sips.sila.org/SIPS/sip-2330)                        | 0x5C   | EXTSLOAD           | Load external contract data                                                  |
| [2936](https://sips.sila.org/SIPS/sip-2936)                        | 0x5C   | EXTCLEAR           | Split storage clearing form SELFDESTRUCT                                     |
| [2937](https://sips.sila.org/SIPS/sip-2937)                        | 0xA8   | SET_INDESTRUCTABLE | Prevents future SELFDESTRUCTs                                                |
| [2938](https://sips.sila.org/SIPS/sip-2938)                        | 0x48   | NONCE              | Get the nonce of the callee                                                  |
| [2938](https://sips.sila.org/SIPS/sip-2938)                        | 0x49   | PAYGAS             | Pays gas for all further operations                                          |
| [2970](https://sips.sila.org/SIPS/sip-2970)                        | 0x4A   | IS_STATIC          | Is current frame static?                                                     |
| [2997](https://sips.sila.org/SIPS/sip-2997)                        | 0xF6   | IMPERAONATECALL    | Call with sender calculated from salt and caller                             |
| [3074](https://sips.sila.org/SIPS/sip-3074)                        | 0xF6   | AUTH               | Preparatory operation for AUTHCALL                                           |
| [3074](https://sips.sila.org/SIPS/sip-3074)                        | 0xF7   | AUTHCALL           | Call with callee set to externally owned account                             |
| [3322](https://sips.sila.org/SIPS/sip-3322)                        | 0x49   | SELFGAS            | Store gas refund to account                                                  |
| [3322](https://sips.sila.org/SIPS/sip-3322)                        | 0x49   | USEGAS             | Increase execution gas from account stored gas                               |
| [3322](https://sips.sila.org/SIPS/sip-3322)                        | 0x49   | STOREGAS           | Move gas to refund                                                           |
| [3332](https://sips.sila.org/SIPS/sip-3332)                        | 0x46   | MEDGASPRICE        | Get median gas price of prior block                                          |
| [3337](https://sips.sila.org/SIPS/sip-3337)                        | 0x5C   | SETFP              | Sets a frame pointer to a memory location                                    |
| [3337](https://sips.sila.org/SIPS/sip-3337)                        | 0x5D   | GETFP              | Gets the current frame pointer                                               |
| [3337](https://sips.sila.org/SIPS/sip-3337)                        | 0x5E   | MLOADFP            | Reads memory at the frame pointer                                            |
| [3337](https://sips.sila.org/SIPS/sip-3337)                        | 0x5F   | MSTOREFP           | Writes memory at the frame pointer                                           |
| [3455](https://sips.sila.org/SIPS/sip-3455)                        | 0xF8   | SUDO               | Unvalidated AUTHCALL (april fools joke)                                      |
| [3508](https://sips.sila.org/SIPS/sip-3508)                        | 0x47   | ORIGINDATALOAD     | Load transaction calldata                                                    |
| [3508](https://sips.sila.org/SIPS/sip-3508)                        | 0x48   | ORIGINDATASIZE     | Size of transaction calldata                                                 |
| [3508](https://sips.sila.org/SIPS/sip-3508)                        | 0x49   | ORIGINDATACOPY     | Bulk load transaction calldata                                               |
| [3520](https://sips.sila.org/SIPS/sip-3520)                        | 0x4A   | ENTRYPOINT         | To address of transaction                                                    |
| [4200](https://sips.sila.org/SIPS/sip-4200)                        | 0xE0   | RJUMP              | relative jump                                                                |
| [4200](https://sips.sila.org/SIPS/sip-4200)                        | 0xE1   | RJUMPI             | relative conditional jump                                                    |
| [4200](https://sips.sila.org/SIPS/sip-4200)                        | 0xE2   | RJUMPV             | relative jump table                                                          |
| [4520](https://sips.sila.org/SIPS/sip-4520)                        | 0xEB   | -                  | Reserve for multi-byte opcodes                                               |
| [4520](https://sips.sila.org/SIPS/sip-4520)                        | 0xEC   | -                  | Reserve for multi-byte opcodes                                               |
| [4750](https://sips.sila.org/SIPS/sip-4750)                        | 0xE3   | CALLF              | EOF Subroutine Call                                                          |
| [4750](https://sips.sila.org/SIPS/sip-4750)                        | 0xE4   | RETF               | EOF Subroutine return                                                        |
| [4788](https://sips.sila.org/SIPS/sip-4788)                        | 0x4A   | BEACON_ROOT        | Exposes the Beacon Chain Root                                                |
| [4844](https://sips.sila.org/SIPS/sip-4844)                        | 0x49   | BLOBHASH           | Returns hashes of blobs in the transaction                                   |
| [5000](https://sips.sila.org/SIPS/sip-5000)                        | 0x1E   | MULDIV             | combo multiply then divide trinary operation                                 |
| [5003](https://sips.sila.org/SIPS/sip-5003)                        | 0xF8   | AUTHUSURP          | Adds code into EOAs                                                          |
| [5478](https://sips.sila.org/SIPS/sip-5478)                        | 0xF6   | CREATE2COPY        | Create 2 with no initcode and contract copying                               |
| [5656](https://sips.sila.org/SIPS/sip-5656)                        | 0xB7   | MCOPY              | Memory copy                                                                  |
| [5920](https://sips.sila.org/SIPS/sip-5920)                        | 0xF9   | PAY                | transfers value from caller to target                                        |
| [6206](https://sips.sila.org/SIPS/sip-6206)                        | 0xE5   | JUMPF              | EOF Function Jump                                                            |
| [6888](https://sips.sila.org/SIPS/sip-6888)                        | 0x5B   | JUMPC              | Jump if the most recent arithmetic op set the carry bit                      |
| [6888](https://sips.sila.org/SIPS/sip-6888)                        | 0x5C   | JUMPO              | Jump if the most recent arithmetic op set the overflow bit                   |
| [6913](https://sips.sila.org/SIPS/sip-6913)                        | 0x49   | SETCODE            | Replace code of current contract                                             |
| [SIP-7069](https://sips.sila.org/SIPS/sip-7069)                    | 0xF7   | RETURNDATALOAD     | Loads data returned from a call to the stack                                 |
| [SIP-7069](https://sips.sila.org/SIPS/sip-7069)                    | 0xF8   | EXTCALL            | CALL without gas and output memory                                           |
| [SIP-7069](https://sips.sila.org/SIPS/sip-7069)                    | 0xF9   | EXTDELEGATECALL    | DELEGATECALL without gas and output memory                                   |
| [SIP-7069](https://sips.sila.org/SIPS/sip-7069)                    | 0xFB   | EXTSTATICCALL      | STATICCALL without gas and output memory                                     |
| [SIP-7480](https://sips.sila.org/SIPS/sip-7480)                    | 0xD0   | DATALOAD           | Loads data from EOF data section, via stack                                  |
| [SIP-7480](https://sips.sila.org/SIPS/sip-7480)                    | 0xD1   | DATALOADN          | Loads data from EOF data section, via immediate                              |
| [SIP-7480](https://sips.sila.org/SIPS/sip-7480)                    | 0xD2   | DATASIZE           | Size of the EOF data section                                                 |
| [SIP-7480](https://sips.sila.org/SIPS/sip-7480)                    | 0xD3   | DATACOPY           | Bulk data section copy                                                       |
| [SIP-7620](https://sips.sila.org/SIPS/sip-7620)                    | 0xEC   | EOFCREATE          | Create from EOF contained initcode                                           |
| [SIP-7620](https://sips.sila.org/SIPS/sip-7620)                    | 0xED   | TXCREATE           | Create from transaction contained initcode (removed from SIP-7620)           |
| [SIP-7620](https://sips.sila.org/SIPS/sip-7620)                    | 0xEE   | RETURNCONTRACT     | Contract to be created, references EOF data                                  |
