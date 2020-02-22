import { Args, Mutation, Query, Resolver, Subscription, ResolveProperty, } from '@nestjs/graphql';
import { EndpointsService } from './endpoints.service';
import { Endpoint } from './models/endpoint';
import { EndpointsArgs } from './dto/endpoints.args';
import { NotFoundException } from '@nestjs/common';

@Resolver(of => Endpoint)
export class EndpointsResolver {
  constructor(private readonly endpointsService: EndpointsService) {}

  @Query(returns => Endpoint, { name: 'endpoint' })
  async endpoint(@Args('id') id: string): Promise<Endpoint> {
      throw new NotFoundException(id)
  }

  @Query(returns => [Endpoint], { name: 'endpoints' })
  async endpoints(@Args() endpointsArgs: EndpointsArgs): Promise<Endpoint[]> {
    return this.endpointsService.findAll(endpointsArgs);
  }

  // @ResolveProperty('hello')
  // getHello(): string {
  //   return this.endpointsService.getHello();
  // }
}
