import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { ObiectProdus } from './Produs'

@Injectable({
  providedIn: 'root'
})
export class RestService {
  
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json'})
  };
  produseUrl : string = "http://127.0.0.1:5000/listaProduse/";

  readProduse(): Observable<ObiectProdus[]>{
    return this.http.get<ObiectProdus[]>(this.produseUrl)
    .pipe(
      catchError(this.handleError<ObiectProdus[]>('readProduse', []))
    );
  }

  addProdus(produs: ObiectProdus){
    console.log("afisare 4:>>>" + produs.name + "=" + produs.price + "=" + produs.stock)
    console.log("afisare 4:>>>" + produs)
    return this.http.post<ObiectProdus>(this.produseUrl, produs);
  }

  deleteProdus(produs: ObiectProdus | number): Observable<ObiectProdus>{
    const id = typeof produs === 'number' ? produs : produs.id;
    const url = `${this.produseUrl}delete/${id}`;
    console.log("produs_id>>" + url)
    // return this.http.delete<ObiectProdus>(url);
    return this.http.get<ObiectProdus>(url);
  }

  updateProdus(produs: ObiectProdus | number): Observable<ObiectProdus>{
    const id = typeof produs === 'number' ? produs : produs.id;
    const url = `${this.produseUrl}update/${id}`;
    console.log("Ai apasat butonul save>rest service te redirectioneaza catre:>>>" + url)
    return this.http.get<ObiectProdus>(url);
  }

  searchProdus(term: string): Observable<ObiectProdus[]> {
    if (!term.trim()) {
      return of([]);
    }
    return this.http.get<ObiectProdus[]>(`${this.produseUrl}/?name=${term}`);
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead
      // TODO: better job of transforming error for user consumption
      console.log(`${operation} failed: ${error.message}`);
      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
  constructor(private http: HttpClient) { }
}
