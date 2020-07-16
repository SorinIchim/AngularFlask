export class ObiectProdus
{
    id: number;
    name: string;
    price: number;
    stock: number;

    constructor(id, name, price, stock)
    {
        this.id = id;
        this.name = name;
        this.price = price;
        this.stock = stock;
    }
}