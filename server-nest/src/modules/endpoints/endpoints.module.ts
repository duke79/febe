import { Module } from '@nestjs/common';
import { EndpointsResolver } from './endpoints.resolver';
import { EndpointsService } from './endpoints.service';

@Module({
  providers: [EndpointsService, EndpointsResolver],
})
export class RequestsModule {}
