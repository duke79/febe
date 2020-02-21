import { Module } from '@nestjs/common';
import { GraphQLModule } from '@nestjs/graphql';
import { RequestsModule } from './modules/endpoints/endpoints.module';

@Module({
  imports: [
    GraphQLModule.forRoot({
      autoSchemaFile: 'schema.gql',
    }),
    RequestsModule,
  ],
})
export class MainModule {}
