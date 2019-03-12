
# from marketplace_processor.protobuf import payload_pb2

# class SmallBankPayload(object):

#     def __init__(self, payload):
#         self._transaction = payload_pb2.TransactionPayload()
#         self._transaction.ParseFromString(payload)

#     def create_account(self):
#         """Returns the value set in the create_account.

#         Returns:
#             payload_pb2.CreateAccount
#         """

#         return self._transaction.create_account

#     def is_create_account(self):

#         create_account = payload_pb2.TransactionPayload.CREATE_ACCOUNT

#         return self._transaction.payload_type == create_account

#     def create_holding(self):
#         """Returns the value set in the create_holding.

#         Returns:
#             payload_pb2.CreateHolding
#         """

#         return self._transaction.create_holding

#     def is_create_holding(self):

#         create_holding = payload_pb2.TransactionPayload.CREATE_HOLDING

#         return self._transaction.payload_type == create_holding

#     def create_asset(self):
#         """Returns the value set in the create_asset.

#         Returns:
#             payload_pb2.CreateAsset
#         """

#         return self._transaction.create_asset

#     def is_create_asset(self):

#         create_asset = payload_pb2.TransactionPayload.CREATE_ASSET

#         return self._transaction.payload_type == create_asset

#     def create_offer(self):
#         """Returns the value set in the create_offer.

#         Returns:
#             payload_pb2.CreateOffer
#         """

#         return self._transaction.create_offer

#     def is_create_offer(self):

#         create_offer = payload_pb2.TransactionPayload.CREATE_OFFER

#         return self._transaction.payload_type == create_offer

#     def accept_offer(self):
#         """Returns the value set in accept_offer.

#         Returns:
#             payload_pb2.AcceptOffer
#         """

#         return self._transaction.accept_offer

#     def is_accept_offer(self):

#         accept_offer = payload_pb2.TransactionPayload.ACCEPT_OFFER

#         return self._transaction.payload_type == accept_offer

#     def close_offer(self):
#         """Returns the value set in close_offer.

#         Returns:
#             payload_pb2.CloseOffer
#         """

#         return self._transaction.close_offer

#     def is_close_offer(self):

#         close_offer = payload_pb2.TransactionPayload.CLOSE_OFFER

#         return self._transaction.payload_type == close_offer


# var logger *logging.Logger = logging.Get()
# var namespace = hexdigest("smallbank")[:6]

# type SmallbankHandler struct {
# }

# func (self *SmallbankHandler) FamilyName() string {
#     return "smallbank"
# }

# func (self *SmallbankHandler) FamilyVersions() []string {
#     return []string{"1.0"}
# }

# func (self *SmallbankHandler) Namespaces() []string {
#     return []string{namespace}
# }

# func (self *SmallbankHandler) Apply(request *processor_pb2.TpProcessRequest, context *processor.Context) error {
#     payload, err := unpackPayload(request.GetPayload())
#     if err != nil {
#         return err
#     }

#     logger.Debugf("smallbank txn %v: type %v",
#         request.Signature, payload.PayloadType)

#     switch payload.PayloadType {
#     case smallbank_pb2.SmallbankTransactionPayload_CREATE_ACCOUNT:
#         return applyCreateAccount(payload.CreateAccount, context)
#     case smallbank_pb2.SmallbankTransactionPayload_DEPOSIT_CHECKING:
#         return applyDepositChecking(payload.DepositChecking, context)
#     case smallbank_pb2.SmallbankTransactionPayload_WRITE_CHECK:
#         return applyWriteCheck(payload.WriteCheck, context)
#     case smallbank_pb2.SmallbankTransactionPayload_TRANSACT_SAVINGS:
#         return applyTransactSavings(payload.TransactSavings, context)
#     case smallbank_pb2.SmallbankTransactionPayload_SEND_PAYMENT:
#         return applySendPayment(payload.SendPayment, context)
#     case smallbank_pb2.SmallbankTransactionPayload_AMALGAMATE:
#         return applyAmalgamate(payload.Amalgamate, context)
#     default:
#         return &processor.InvalidTransactionError{
#             Msg: fmt.Sprintf("Invalid PayloadType: '%v'", payload.PayloadType)}
#     }
# }

# func applyCreateAccount(createAccountData *smallbank_pb2.SmallbankTransactionPayload_CreateAccountTransactionData, context *processor.Context) error {
#     account, err := loadAccount(createAccountData.CustomerId, context)
#     if err != nil {
#         return err
#     }

#     if account != nil {
#         return &processor.InvalidTransactionError{Msg: "Account already exists"}
#     }

#     if createAccountData.CustomerName == "" {
#         return &processor.InvalidTransactionError{Msg: "Customer Name must be set"}
#     }

#     new_account := &smallbank_pb2.Account{
#         CustomerId:      createAccountData.CustomerId,
#         CustomerName:    createAccountData.CustomerName,
#         SavingsBalance:  createAccountData.InitialSavingsBalance,
#         CheckingBalance: createAccountData.InitialCheckingBalance,
#     }

#     saveAccount(new_account, context)

#     return nil
# }

# func applyDepositChecking(depositCheckingData *smallbank_pb2.SmallbankTransactionPayload_DepositCheckingTransactionData, context *processor.Context) error {
#     account, err := loadAccount(depositCheckingData.CustomerId, context)
#     if err != nil {
#         return err
#     }

#     if account == nil {
#         return &processor.InvalidTransactionError{Msg: "Account must exist"}
#     }

#     new_account := &smallbank_pb2.Account{
#         CustomerId:      account.CustomerId,
#         CustomerName:    account.CustomerName,
#         SavingsBalance:  account.SavingsBalance,
#         CheckingBalance: account.CheckingBalance + depositCheckingData.Amount,
#     }

#     saveAccount(new_account, context)

#     return nil
# }

# func applyWriteCheck(writeCheckData *smallbank_pb2.SmallbankTransactionPayload_WriteCheckTransactionData, context *processor.Context) error {
#     account, err := loadAccount(writeCheckData.CustomerId, context)
#     if err != nil {
#         return err
#     }

#     if account == nil {
#         return &processor.InvalidTransactionError{Msg: "Account must exist"}
#     }

#     new_account := &smallbank_pb2.Account{
#         CustomerId:      account.CustomerId,
#         CustomerName:    account.CustomerName,
#         SavingsBalance:  account.SavingsBalance,
#         CheckingBalance: account.CheckingBalance - writeCheckData.Amount,
#     }

#     saveAccount(new_account, context)

#     return nil
# }

# func applyTransactSavings(transactSavingsData *smallbank_pb2.SmallbankTransactionPayload_TransactSavingsTransactionData, context *processor.Context) error {
#     account, err := loadAccount(transactSavingsData.CustomerId, context)
#     if err != nil {
#         return err
#     }

#     if account == nil {
#         return &processor.InvalidTransactionError{Msg: "Account must exist"}
#     }

#     var new_balance uint32

#     if transactSavingsData.Amount < 0 {
#         if uint32(-transactSavingsData.Amount) > account.SavingsBalance {
#             return &processor.InvalidTransactionError{Msg: "Insufficient funds in source savings account"}
#         }
#         new_balance = account.SavingsBalance - uint32(-transactSavingsData.Amount)
#     } else {
#         new_balance = account.SavingsBalance + uint32(transactSavingsData.Amount)
#     }

#     new_account := &smallbank_pb2.Account{
#         CustomerId:      account.CustomerId,
#         CustomerName:    account.CustomerName,
#         SavingsBalance:  new_balance,
#         CheckingBalance: account.CheckingBalance,
#     }

#     saveAccount(new_account, context)

#     return nil
# }

# func applySendPayment(sendPaymentData *smallbank_pb2.SmallbankTransactionPayload_SendPaymentTransactionData, context *processor.Context) error {
#     source_account, err := loadAccount(sendPaymentData.SourceCustomerId, context)
#     if err != nil {
#         return err
#     }

#     dest_account, err := loadAccount(sendPaymentData.DestCustomerId, context)
#     if err != nil {
#         return err
#     }

#     if source_account == nil || dest_account == nil {
#         return &processor.InvalidTransactionError{Msg: "Both source and dest accounts must exist"}
#     }

#     if source_account.CheckingBalance < sendPaymentData.Amount {
#         return &processor.InvalidTransactionError{Msg: "Insufficient funds in source checking account"}
#     }

#     new_source_account := &smallbank_pb2.Account{
#         CustomerId:      source_account.CustomerId,
#         CustomerName:    source_account.CustomerName,
#         SavingsBalance:  source_account.SavingsBalance,
#         CheckingBalance: source_account.CheckingBalance - sendPaymentData.Amount,
#     }

#     new_dest_account := &smallbank_pb2.Account{
#         CustomerId:      dest_account.CustomerId,
#         CustomerName:    dest_account.CustomerName,
#         SavingsBalance:  dest_account.SavingsBalance,
#         CheckingBalance: dest_account.CheckingBalance + sendPaymentData.Amount,
#     }

#     saveAccount(new_source_account, context)
#     saveAccount(new_dest_account, context)

#     return nil
# }

# func applyAmalgamate(amalgamateData *smallbank_pb2.SmallbankTransactionPayload_AmalgamateTransactionData, context *processor.Context) error {
#     source_account, err := loadAccount(amalgamateData.SourceCustomerId, context)
#     if err != nil {
#         return err
#     }

#     dest_account, err := loadAccount(amalgamateData.DestCustomerId, context)
#     if err != nil {
#         return err
#     }

#     if source_account == nil || dest_account == nil {
#         return &processor.InvalidTransactionError{Msg: "Both source and dest accounts must exist"}
#     }

#     new_source_account := &smallbank_pb2.Account{
#         CustomerId:      source_account.CustomerId,
#         CustomerName:    source_account.CustomerName,
#         SavingsBalance:  0,
#         CheckingBalance: source_account.CheckingBalance,
#     }

#     new_dest_account := &smallbank_pb2.Account{
#         CustomerId:      dest_account.CustomerId,
#         CustomerName:    dest_account.CustomerName,
#         SavingsBalance:  dest_account.SavingsBalance,
#         CheckingBalance: dest_account.CheckingBalance + source_account.SavingsBalance,
#     }

#     saveAccount(new_source_account, context)
#     saveAccount(new_dest_account, context)

#     return nil
# }

# func unpackPayload(payloadData []byte) (*smallbank_pb2.SmallbankTransactionPayload, error) {
#     payload := &smallbank_pb2.SmallbankTransactionPayload{}
#     err := proto.Unmarshal(payloadData, payload)
#     if err != nil {
#         return nil, &processor.InternalError{
#             Msg: fmt.Sprint("Failed to unmarshal SmallbankTransaction: %v", err)}
#     }
#     return payload, nil
# }

# func unpackAccount(accountData []byte) (*smallbank_pb2.Account, error) {
#     account := &smallbank_pb2.Account{}
#     err := proto.Unmarshal(accountData, account)
#     if err != nil {
#         return nil, &processor.InternalError{
#             Msg: fmt.Sprint("Failed to unmarshal Account: %v", err)}
#     }
#     return account, nil
# }

# func loadAccount(customer_id uint32, context *processor.Context) (*smallbank_pb2.Account, error) {
#     address := namespace + hexdigest(fmt.Sprint(customer_id))[:64]

#     results, err := context.GetState([]string{address})
#     if err != nil {
#         return nil, err
#     }

#     if len(string(results[address])) > 0 {
#         account, err := unpackAccount(results[address])
#         if err != nil {
#             return nil, err
#         }

#         return account, nil
#     }
#     return nil, nil
# }

# func saveAccount(account *smallbank_pb2.Account, context *processor.Context) error {
#     address := namespace + hexdigest(fmt.Sprint(account.CustomerId))[:64]
#     data, err := proto.Marshal(account)
#     if err != nil {
#         return &processor.InternalError{Msg: fmt.Sprint("Failed to serialize Account:", err)}
#     }

#     addresses, err := context.SetState(map[string][]byte{
#         address: data,
#     })
#     if err != nil {
#         return err
#     }

#     if len(addresses) == 0 {
#         return &processor.InternalError{Msg: "No addresses in set response"}
#     }
#     return nil
# }

# func hexdigest(str string) string {
#     hash := sha512.New()
#     hash.Write([]byte(str))
#     hashBytes := hash.Sum(nil)
#     return strings.ToLower(hex.EncodeToString(hashBytes))
# }