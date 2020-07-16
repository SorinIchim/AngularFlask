import { Component, OnInit, Input } from '@angular/core';
import { RestService } from './rest.service';
import { ObiectProdus } from './Produs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {
  title = 'AngularFlask';
  @Input() produse: ObiectProdus[] = [];
  // produse : ObiectProdus[] = [];
  searchText;
  constructor(private rs : RestService){}

  headers = ["id","name", "price",  "stock"]

  ngOnInit()
{
      this.rs.readProduse()
      .subscribe
        (
          (response) => 
          {
            this.produse = response;
          },
          (error) =>
          {
            console.log("No Data Found" + error);
          }

        )
}

add(name: string, price: number, stock: number): void {
  if (!name) { return; }
  console.log("afisare 1:>>>" + name + "=" + price + "=" + stock)
  this.rs.addProdus({ name, price, stock } as ObiectProdus)
    .subscribe(produs => {
      console.log("afisare 2:>>>" + name + "=" + price + "=" + stock)
      this.produse.push(produs);
      console.log("afisare 3:>>>" + name + "=" + price + "=" + stock)
      console.log("afisare 3:>>>" + produs)
    });
}

delete(produs: ObiectProdus): void {
  this.produse = this.produse.filter(h => h !== produs);
  this.rs.deleteProdus(produs).subscribe();
}

update(produs: ObiectProdus): void {
  this.produse = this.produse.filter(h => h !== produs);
  console.log("Ai apasat butonul save>app.component.ts apeleaza RS.updateProdus(produs) | Nume produs>>>" + produs.name);
  this.rs.updateProdus(produs).subscribe();
}
}