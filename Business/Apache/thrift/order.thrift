namespace py order_service

service OrderProcessingService {
    string calculate_total(1:string product_id, 2:i32 quantity)
}