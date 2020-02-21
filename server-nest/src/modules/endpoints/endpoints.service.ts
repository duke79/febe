import { Injectable } from '@nestjs/common';
import { EndpointsArgs } from './dto/endpoints.args';
import { Endpoint } from './models/endpoint';

@Injectable()
export class EndpointsService {
  getHello(): string {
    return 'Hello World!';
  }

  async findAll(endpointsArgs: EndpointsArgs): Promise<Endpoint[]> {
    return [] as Endpoint[];
  }
}
